"""Support ticket triage service. Cost-optimized reference implementation.

This is the *reference solution* for the fixture: the version an agent
applying the nine techniques should converge on. The harness scores any
candidate against `ticket_service.py`; this file exists to establish the
achievable ceiling and to prove the metric responds to each technique.

Change log against the original, by technique:

  1  Success defined as exact (category, priority) match. Encoded in the
     harness, which is what makes any of the rest verifiable.
  2  Per-call telemetry emitted: tier, cached fraction, escalation, outcome.
  3  Timestamp and request id moved behind the static prefix. Prefix is now
     byte-identical across requests, so it caches.
  4  Tool schemas filtered to those the task can reach. Classification calls
     need none, so none are sent.
  5  Verified escalation: flash first, structural verify, escalate to pro on
     failure. Escalation rate instrumented as a kill criterion.
  6  Iteration cap. No unbounded loop.
  7  Nightly summaries moved to the batch path.
  8  Structured output with a schema and an output cap, replacing free-form
     reasoning that was discarded by a regex.
  9  Interactive classification on standard tier; the nightly job on batch.

Note on technique 5's dependency: the deterministic verifier is only possible
because technique 8's structured output makes the response machine-checkable.
Free-form prose has nothing to validate against.
"""

from __future__ import annotations

import dataclasses
import datetime
import json

from fake_model import FakeModel
from fake_model import is_structurally_valid
from ticket_service import ESCALATION_POLICY
from ticket_service import TOOL_SCHEMAS

MAX_ATTEMPTS = 2
MAX_OUTPUT_TOKENS = 32

# T3: the static prefix now leads. Nothing variable precedes it, so the
# platform sees an identical prefix on every request and the cache engages.
STATIC_PREFIX = (
    "You are a support triage assistant.\n\n"
    + __import__("ticket_service").CATEGORY_GUIDE
    + "\n\n"
    + ESCALATION_POLICY
    + "\n"
)


@dataclasses.dataclass
class Telemetry:
    """T2: per-request record. Cost data alone cannot reconstruct this."""

    ticket_id: str
    tier: str
    escalated: bool
    prompt_tokens: int
    cached_tokens: int
    output_tokens: int
    valid: bool


TELEMETRY: list[Telemetry] = []


def tools_for(task: str) -> list[dict]:
    """T4: load tools by task, not the whole registry.

    Classification is a labelling task -- it takes no actions, so it needs no
    tool schemas at all. Sending 60+ of them cost tokens and, above a few
    dozen, degrades tool-selection accuracy too.
    """
    if task == "classify":
        return []
    return TOOL_SCHEMAS


def build_prompt(ticket, *, with_context: bool) -> str:
    """T3: static content first, variable content last."""
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    parts = [STATIC_PREFIX]
    tools = tools_for("classify")
    if tools:
        parts.append(f"AVAILABLE_TOOLS:\n{json.dumps(tools)}")
    parts.append(
        "Respond only with JSON: "
        '{"category": <CATEGORY>, "priority": "P0"|"P1"|"P2"|"P3"}'
    )
    if with_context:
        parts.append(f"ACCOUNT_CONTEXT: {json.dumps(ticket.account_context)}")
    parts.append(f"TICKET: {ticket.text}")
    parts.append(f"Request timestamp: {now}\nRequest id: {ticket.id}")
    return "\n\n".join(parts)


def parse_response(text: str) -> tuple[str, str]:
    """T8: structured output means parsing is total, not a partial regex."""
    try:
        d = json.loads(text)
        return d["category"], d["priority"]
    except (json.JSONDecodeError, KeyError, TypeError):
        return "GENERAL_INQUIRY", "P3"


def classify(ticket, model: FakeModel) -> tuple[str, str]:
    """T5: route cheap, verify, escalate on observed failure.

    Difficulty is not predicted from the ticket text. The cheap tier answers
    first and the answer is checked; escalation is triggered by a failed
    check, not by a guess about what the text implies. Worst case is two
    calls -- bounded and measurable -- rather than an unbounded, invisible
    quality loss.
    """
    # Account context is retrieved unconditionally. It is the discriminator
    # for every hard ticket, and no model tier can substitute for a fact that
    # was never sent.
    prompt = build_prompt(ticket, with_context=True)

    cat = prio = None
    escalated = False

    # T6: explicit ceiling. The loop cannot run away.
    for attempt in range(MAX_ATTEMPTS):
        tier = "flash" if attempt == 0 else "pro"
        text, u = model.generate(
            prompt,
            model=tier,
            response_schema=True,  # T8
            max_output_tokens=MAX_OUTPUT_TOKENS,  # T8
            ticket=ticket,
            path="classify",
        )
        cat, prio = parse_response(text)
        ok = is_structurally_valid(cat, prio)

        TELEMETRY.append(
            Telemetry(
                ticket_id=ticket.id,
                tier=tier,
                escalated=attempt > 0,
                prompt_tokens=u.prompt_token_count,
                cached_tokens=u.cached_content_token_count,
                output_tokens=u.candidates_token_count,
                valid=ok,
            )
        )

        if ok:
            return cat, prio
        escalated = True

    return cat or "GENERAL_INQUIRY", prio or "P3"


def nightly_summary(tickets, model: FakeModel) -> list[str]:
    """T7 + T9: off the live path, on the batch tier.

    Nobody is waiting on the morning report. Running it synchronously against
    the interactive endpoint made it compete for rate-limit headroom with
    requests where someone was.
    """
    out = []
    for t in tickets:
        text, _ = model.generate(
            f"{STATIC_PREFIX}\nSummarize in one line: {t.text}",
            model="flash",
            batch=True,
            max_output_tokens=24,
            path="nightly",
        )
        out.append(text)
    return out


def escalation_rate() -> float:
    """T5 kill criterion. Above ~0.5 the cascade has inverted."""
    if not TELEMETRY:
        return 0.0
    esc = sum(1 for t in TELEMETRY if t.escalated)
    tickets = len({t.ticket_id for t in TELEMETRY})
    return esc / tickets if tickets else 0.0


def run(tickets, model: FakeModel) -> dict[str, tuple[str, str]]:
    TELEMETRY.clear()
    results = {t.id: classify(t, model) for t in tickets}
    nightly_summary(tickets, model)
    return results
