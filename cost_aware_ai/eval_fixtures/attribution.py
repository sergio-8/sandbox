"""Per-technique attribution: fix one defect at a time, measure the delta.

Answers "what is each technique worth here", and — more importantly —
verifies that the metric is actually sensitive to each one. A technique that
moves nothing is either not exercised by the fixture or not measurable by
this harness, and either way the fixture should be fixed rather than the
result reported.

Runs each variant against the same corpus. Deterministic.
"""

from __future__ import annotations

import datetime
import json

from corpus import build_corpus
from corpus import daily_volume
from fake_model import FakeModel
from fake_model import is_structurally_valid
import ticket_service as naive
import ticket_service_patched as fixed


def _cost(fn, tickets):
    m = FakeModel()
    preds = fn(tickets, m)
    by_id = {t.id: t for t in tickets}
    correct = sum(
        1
        for tid, (c, p) in preds.items()
        if c == by_id[tid].label_category and p == by_id[tid].label_priority
    )
    cost = sum(u.cost_usd() for u in m.calls)
    billed = sum(
        u.prompt_token_count - u.cached_content_token_count + u.candidates_token_count
        for u in m.calls
    )
    return {
        "cost": cost,
        "correct": correct,
        "acc": correct / len(tickets),
        "cpc": cost / correct if correct else float("inf"),
        "billed": billed,
    }


# --- single-technique variants -------------------------------------------
# Each starts from the naive service and repairs exactly one defect.


def v_t3_cache_only(tickets, model):
    """T3 alone: move the timestamp behind the static prefix."""
    results = {}
    for t in tickets:
        prompt = (
            f"{naive.STATIC_PREFIX}\n"
            f"AVAILABLE_TOOLS:\n{json.dumps(naive.TOOL_SCHEMAS)}\n\n"
            f"Think step by step and explain your reasoning in full.\n\n"
            f"TICKET: {t.text}\n"
            f"Request timestamp: "
            f"{datetime.datetime.now(datetime.timezone.utc).isoformat()}\n"
        )
        text, _ = model.generate(prompt, model="pro", ticket=t, path="classify")
        results[t.id] = naive.parse_response(text)
    naive.nightly_summary(tickets, model)
    return results


def v_t4_tools_only(tickets, model):
    """T4 alone: stop sending 60+ tool schemas to a labelling task."""
    results = {}
    for t in tickets:
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        prompt = (
            f"Request timestamp: {now}\nRequest id: {t.id}-{now}\n"
            f"{naive.STATIC_PREFIX}\n"
            f"Think step by step and explain your reasoning in full.\n\n"
            f"TICKET: {t.text}\n"
        )
        text, _ = model.generate(prompt, model="pro", ticket=t, path="classify")
        results[t.id] = naive.parse_response(text)
    naive.nightly_summary(tickets, model)
    return results


def v_t5_tier_only(tickets, model):
    """T5 alone: flagship -> flash, no verification, no escalation.

    This is the Pareto trap in miniature: cost falls, and the harness should
    show quality falling with it.
    """
    results = {}
    for t in tickets:
        prompt = naive.build_prompt(t)
        text, _ = model.generate(prompt, model="flash", ticket=t, path="classify")
        results[t.id] = naive.parse_response(text)
    naive.nightly_summary(tickets, model)
    return results


def v_t5_escalation(tickets, model):
    """T5 done properly: cheap first, verify, escalate on failure."""
    results = {}
    for t in tickets:
        prompt = naive.build_prompt(t)
        for attempt in range(2):
            tier = "flash" if attempt == 0 else "pro"
            text, _ = model.generate(prompt, model=tier, ticket=t, path="classify")
            c, p = naive.parse_response(text)
            if is_structurally_valid(c, p):
                break
        results[t.id] = (c, p)
    naive.nightly_summary(tickets, model)
    return results


def v_t5b_plus_t8(tickets, model):
    """T5 escalation *with* T8 structured output.

    T5b alone barely moves accuracy, because the naive regex parser mangles
    the response before the verifier ever sees it — the verifier is checking
    the parser's guess, not the model's answer. Escalation only works once
    the response is machine-readable. This pair demonstrates that the
    techniques are not independent line items.
    """
    results = {}
    for t in tickets:
        prompt = naive.build_prompt(t)
        for attempt in range(2):
            tier = "flash" if attempt == 0 else "pro"
            text, _ = model.generate(
                prompt,
                model=tier,
                response_schema=True,
                max_output_tokens=32,
                ticket=t,
                path="classify",
            )
            c, p = fixed.parse_response(text)
            if is_structurally_valid(c, p):
                break
        results[t.id] = (c, p)
    naive.nightly_summary(tickets, model)
    return results


def v_t8_output_only(tickets, model):
    """T8 alone: structured output + cap, replacing discarded prose."""
    results = {}
    for t in tickets:
        prompt = naive.build_prompt(t)
        text, _ = model.generate(
            prompt,
            model="pro",
            response_schema=True,
            max_output_tokens=32,
            ticket=t,
            path="classify",
        )
        results[t.id] = fixed.parse_response(text)
    naive.nightly_summary(tickets, model)
    return results


def v_t7_batch_only(tickets, model):
    """T7 alone: nightly job to the batch tier."""
    results = {}
    for t in tickets:
        results[t.id] = naive.classify(t, model)
    for t in tickets:
        model.generate(
            f"{naive.STATIC_PREFIX}\nSummarize in one line: {t.text}",
            model="flash",
            batch=True,
            max_output_tokens=24,
            path="nightly",
        )
    return results


def v_context_only(tickets, model):
    """Retrieve account context. Not one of the nine, but the accuracy lever.

    Included to show the metric separates *cost* levers from *quality*
    levers: this one should raise cost slightly and accuracy sharply.
    """
    results = {}
    for t in tickets:
        prompt = (
            naive.build_prompt(t)
            + f"\nACCOUNT_CONTEXT: {json.dumps(t.account_context)}"
        )
        text, _ = model.generate(prompt, model="pro", ticket=t, path="classify")
        results[t.id] = naive.parse_response(text)
    naive.nightly_summary(tickets, model)
    return results


VARIANTS = [
    ("baseline (all 9 defects)", naive.run),
    ("T3  cache: prefix fixed", v_t3_cache_only),
    ("T4  tools: registry pruned", v_t4_tools_only),
    ("T5a tier: flagship->flash", v_t5_tier_only),
    ("T5b tier: verified escalation", v_t5_escalation),
    ("T7  batch: nightly offline", v_t7_batch_only),
    ("T8  output: schema + cap", v_t8_output_only),
    ("T5b+T8 escalation on schema", v_t5b_plus_t8),
    ("--  retrieval: context sent", v_context_only),
    ("ALL techniques applied", fixed.run),
]


def main() -> None:
    tickets = build_corpus()
    base = _cost(naive.run, tickets)
    scale = daily_volume() / len(tickets) * 30

    print(
        f"\n{'variant':32s} {'acc':>7s} {'billed':>12s} "
        f"{'$/correct':>11s} {'vs base':>9s}  {'$/mo':>9s}"
    )
    print("-" * 88)
    for name, fn in VARIANTS:
        r = _cost(fn, tickets)
        delta = 1 - r["cpc"] / base["cpc"]
        flag = ""
        if r["acc"] < base["acc"] - 1e-9:
            flag = "  <- quality regression"
        print(
            f"{name:32s} {r['acc']:6.1%} {r['billed']:12,d} "
            f"{r['cpc']:11.6f} {delta:+8.1%}  {r['cost'] * scale:8,.0f}{flag}"
        )
    print("-" * 88)
    print(
        "\nRead the T5a row against T5b. Both cut the model bill; only one is\n"
        "an improvement. A harness reporting cost alone would rank them the\n"
        "same way, which is the failure the denominator exists to prevent."
    )


if __name__ == "__main__":
    main()
