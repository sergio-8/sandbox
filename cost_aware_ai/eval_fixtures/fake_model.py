"""Deterministic model simulator with a real prefix cache and a real biller.

Nothing here calls a network. Every number the harness reports is produced by
counting, so two runs of the same code produce identical totals. That is the
point: the metric must have no variance contributed by the measuring
instrument.

Two behaviours are modelled faithfully because the evaluation depends on them:

1.  **Caching is a prefix match.** `_cached_prefix_len` walks the tokenised
    request from position zero and stops at the first divergence. A request
    whose first token varies per call therefore has a shared prefix of length
    zero, no matter how many thousand identical tokens follow it. This is why
    the planted timestamp defect costs real money in this simulation rather
    than being a stylistic complaint.

2.  **Tier capability is a function of the information present in the
    request.** A cheap model cannot resolve a ticket whose discriminator was
    never included, and neither can an expensive one. Spending more on a
    request that omits the deciding fact does not buy correctness -- so a
    model-tier upgrade cannot paper over a retrieval bug.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import re

from corpus import CATEGORIES
from corpus import PRIORITY_BAND

# Per-million-token prices. Ratios reflect published Vertex tier structure;
# absolute values are arbitrary and cancel out of every comparison.
PRICING = {
    "flash": {"in": 0.30, "cached_in": 0.075, "out": 2.50},
    "pro": {"in": 2.50, "cached_in": 0.625, "out": 15.00},
}
BATCH_DISCOUNT = 0.50

# Cached input is 25% of standard input in both tiers -- so a forfeited cache
# hit costs 4x, which is what makes defect 3 the expensive one.


@dataclasses.dataclass
class Usage:
    """Mirrors the shape of a real `usage_metadata` object."""

    prompt_token_count: int = 0
    cached_content_token_count: int = 0
    candidates_token_count: int = 0
    total_token_count: int = 0
    model: str = ""
    batch: bool = False
    path: str = "unknown"  # which call site produced this

    def cost_usd(self) -> float:
        p = PRICING[self.model]
        fresh = self.prompt_token_count - self.cached_content_token_count
        c = (
            fresh * p["in"]
            + self.cached_content_token_count * p["cached_in"]
            + self.candidates_token_count * p["out"]
        ) / 1_000_000
        return c * (BATCH_DISCOUNT if self.batch else 1.0)


def tokenize(text: str) -> list[str]:
    """~4 chars/token, whitespace-aligned. Deterministic."""
    return re.findall(r"\S+", text)


class FakeModel:
    """A callable model with a prefix cache and a usage ledger."""

    def __init__(self) -> None:
        self.calls: list[Usage] = []
        self._prefix_cache: list[list[str]] = []

    # -- cache -------------------------------------------------------------

    def _cached_prefix_len(self, toks: list[str]) -> int:
        best = 0
        for entry in self._prefix_cache:
            n = 0
            for a, b in zip(entry, toks):
                if a != b:
                    break
                n += 1
            best = max(best, n)
        # Platforms only cache above a minimum block size.
        return best if best >= 256 else 0

    def _remember(self, toks: list[str]) -> None:
        self._prefix_cache.append(toks)
        if len(self._prefix_cache) > 8:
            self._prefix_cache.pop(0)

    # -- generation --------------------------------------------------------

    def generate(
        self,
        prompt: str,
        *,
        model: str = "flash",
        max_output_tokens: int | None = None,
        response_schema: bool = False,
        batch: bool = False,
        ticket=None,
        path: str = "unknown",
    ) -> tuple[str, Usage]:
        """Return (response_text, usage).

        `ticket` is the ground-truth object, used only to decide whether the
        *information required* to answer is present in `prompt`. The model
        never reads the label. This keeps the simulation honest: it models
        capability, it does not leak answers.
        """
        toks = tokenize(prompt)
        cached = self._cached_prefix_len(toks)
        self._remember(toks)

        text = self._answer(prompt, model, response_schema, ticket)
        if max_output_tokens is not None:
            out_toks = tokenize(text)[:max_output_tokens]
            text = " ".join(out_toks)
        out_n = len(tokenize(text))

        u = Usage(
            prompt_token_count=len(toks),
            cached_content_token_count=cached,
            candidates_token_count=out_n,
            total_token_count=len(toks) + out_n,
            model=model,
            batch=batch,
            path=path,
        )
        self.calls.append(u)
        return text, u

    # -- capability model --------------------------------------------------

    def _answer(self, prompt, model, response_schema, ticket) -> str:
        if ticket is None:
            return "OK"

        ctx_present = "ACCOUNT_CONTEXT" in prompt
        correct = self._would_be_correct(ticket, ctx_present, model)

        if correct:
            cat, prio = ticket.label_category, ticket.label_priority
        else:
            cat, prio = self._plausible_wrong(ticket, ctx_present)

        if response_schema:
            return json.dumps({"category": cat, "priority": prio})
        # Free-form: the verbose reasoning the naive service asks for and
        # then throws away.
        return (
            f"Let me work through this ticket carefully. The customer writes: "
            f"{ticket.text!r} I will consider each of the twelve categories in "
            f"turn and weigh the evidence for and against, then settle on the "
            f"one that best fits the situation described. Taking account of "
            f"tone, urgency and the specific nouns used, and comparing against "
            f"similar tickets I have seen, I believe the most defensible "
            f"reading here is as follows. "
            f"Category: {cat}. Priority: {prio}."
        )

    @staticmethod
    def _would_be_correct(ticket, ctx_present: bool, model: str) -> bool:
        """Capability rule. Deterministic, no randomness."""
        if ticket.difficulty == "easy":
            # Both tiers handle unambiguous surface text.
            return True

        if not ctx_present:
            # The discriminator was never sent. No tier can recover it.
            # For collision pairs the text is byte-identical, so the best any
            # text-only classifier can do is answer the same way for both
            # members -- exactly 50%. We model that by letting the first
            # member of each pair land and the second miss.
            if ticket.collision_group is not None:
                return int(ticket.id[1:]) % 2 == 0
            # Non-collision hard tickets: flagship guesses better than flash
            # from surface cues alone, but neither is reliable.
            return (int(ticket.id[1:]) % 3 == 0) if model == "pro" else False

        # Context supplied: the discriminating fields are in the prompt.
        if model == "pro":
            return True
        # Flash resolves context-bearing tickets except the subtlest pairs.
        return ticket.collision_group is None or int(ticket.id[1:]) % 2 == 0

    @staticmethod
    def _plausible_wrong(ticket, ctx_present: bool) -> tuple[str, str]:
        """A wrong answer that is *superficially* reasonable.

        Deliberately biased toward the low-severity reading, which is the
        real-world failure shape: a fraud report filed as a billing question.
        """
        h = int(hashlib.md5(ticket.id.encode()).hexdigest(), 16)
        benign = ("BILLING_QUESTION", "GENERAL_INQUIRY", "SHIPPING_DELAY")
        cat = benign[h % len(benign)]
        # A model that mislabels also sometimes emits a priority inconsistent
        # with its own chosen category. Roughly a third of errors have this
        # shape, and those are the ones a structural check can catch for free.
        # The remaining two thirds are self-consistent and therefore invisible
        # to any verifier that does not know the answer -- which is the honest
        # ceiling on what deterministic verification buys you.
        prio = "P1" if h % 3 == 0 else "P3"
        return cat, prio


def is_structurally_valid(cat: str, prio: str) -> bool:
    """Deterministic verifier available to any implementation.

    Checks only what can be checked without the answer: is the category in
    the enum, and is the priority inside that category's permitted band?
    This is what technique 5's verified escalation is built on -- it catches
    a meaningful share of errors at zero model cost.
    """
    if cat not in CATEGORIES:
        return False
    return prio in PRIORITY_BAND.get(cat, set())
