"""Execution-based grader for the cost-aware-ai skill.

    python3 harness.py --impl ticket_service            # baseline
    python3 harness.py --impl ticket_service_patched    # candidate
    python3 harness.py --compare ticket_service ticket_service_patched

The headline metric is

    cost_per_correct = total_cost_usd / n_correct

Every term is counted, not judged. Tokens come from the usage ledger,
correctness from exact match against generated labels. Two runs of the same
implementation produce byte-identical output.

`cost_per_correct` is used rather than raw cost because raw cost alone is
trivially gamed -- returning a constant string costs almost nothing. The
denominator is what stops the metric from rewarding a cheaper, worse system,
and it is the mechanical form of the skill's own governing constraint.

A candidate must clear an accuracy floor to be scored at all. Buying cost
reduction with accuracy is the specific failure the skill exists to prevent,
so the harness refuses to report a win that was paid for that way.
"""

from __future__ import annotations

import argparse
import importlib
import json
import sys

from corpus import build_corpus
from corpus import daily_volume
from fake_model import FakeModel

ACCURACY_FLOOR = 0.90  # fraction of the baseline's accuracy


def evaluate(module_name: str, tickets) -> dict:
    """Run one implementation over the corpus and count everything."""
    mod = importlib.import_module(module_name)
    model = FakeModel()

    preds = mod.run(tickets, model)

    by_id = {t.id: t for t in tickets}
    correct = cat_correct = 0
    collision_total = collision_correct = 0
    p0_missed = 0

    for tid, (cat, prio) in preds.items():
        t = by_id[tid]
        cat_ok = cat == t.label_category
        cat_correct += cat_ok
        full_ok = cat_ok and prio == t.label_priority
        correct += full_ok
        if t.collision_group is not None:
            collision_total += 1
            collision_correct += full_ok
        # Severity inversion: a P0 downgraded is the expensive kind of wrong.
        if t.label_priority == "P0" and prio != "P0":
            p0_missed += 1

    n = len(tickets)
    tokens_in = sum(u.prompt_token_count for u in model.calls)
    tokens_cached = sum(u.cached_content_token_count for u in model.calls)
    tokens_out = sum(u.candidates_token_count for u in model.calls)
    cost = sum(u.cost_usd() for u in model.calls)

    # Cache hit rate on the interactive path only. Reported separately
    # because a self-caching background job otherwise inflates the aggregate
    # and hides a live path that is caching nothing -- which is exactly the
    # defect under test.
    live = [u for u in model.calls if u.path == "classify"]
    live_in = sum(u.prompt_token_count for u in live)
    live_cached = sum(u.cached_content_token_count for u in live)

    # Escalation rate: calls beyond the first per ticket on the live path.
    escalations = max(0, len(live) - n)

    billable_in = tokens_in - tokens_cached
    scale = daily_volume() / n

    return {
        "impl": module_name,
        "n_tickets": n,
        "n_calls": len(model.calls),
        "calls_per_ticket": len(model.calls) / n,
        "accuracy": correct / n,
        "category_accuracy": cat_correct / n,
        "collision_accuracy": (
            collision_correct / collision_total if collision_total else None
        ),
        "p0_missed": p0_missed,
        "tokens_in": tokens_in,
        "tokens_cached": tokens_cached,
        "tokens_out": tokens_out,
        "cache_hit_rate": tokens_cached / tokens_in if tokens_in else 0.0,
        "live_cache_hit_rate": live_cached / live_in if live_in else 0.0,
        "escalation_rate": escalations / n,
        "total_tokens_billed": billable_in + tokens_out,
        "cost_usd": cost,
        "cost_per_correct": (cost / correct) if correct else float("inf"),
        "projected_daily_usd": cost * scale,
        "projected_monthly_usd": cost * scale * 30,
    }


def _fmt(r: dict) -> str:
    ca = r["collision_accuracy"]
    return "\n".join(
        [
            f"  accuracy              {r['accuracy']:.1%}"
            f"   (category only {r['category_accuracy']:.1%})",
            f"  collision subset      {ca:.1%}" if ca is not None else "",
            f"  P0 downgraded         {r['p0_missed']}",
            f"  model calls           {r['n_calls']}  "
            f"({r['calls_per_ticket']:.2f}/ticket)",
            f"  escalation rate       {r['escalation_rate']:.1%}"
            + ("   KILL CRITERION BREACHED" if r["escalation_rate"] > 0.5 else ""),
            f"  cache hit (live path) {r['live_cache_hit_rate']:.1%}",
            f"  tokens billed         {r['total_tokens_billed']:,}",
            f"  cost (150 tickets)    ${r['cost_usd']:.4f}",
            f"  COST PER CORRECT      ${r['cost_per_correct']:.6f}",
            f"  projected monthly     ${r['projected_monthly_usd']:,.0f}"
            f"   @ {daily_volume():,}/day",
        ]
    ).replace("\n\n", "\n")


def compare(base_name: str, cand_name: str, tickets) -> int:
    base = evaluate(base_name, tickets)
    cand = evaluate(cand_name, tickets)

    print(f"\nBASELINE  {base_name}")
    print(_fmt(base))
    print(f"\nCANDIDATE {cand_name}")
    print(_fmt(cand))

    floor = base["accuracy"] * ACCURACY_FLOOR
    print("\n" + "-" * 60)

    if cand["accuracy"] < floor:
        print(
            f"REJECTED. Accuracy {cand['accuracy']:.1%} is below the floor of "
            f"{floor:.1%} ({ACCURACY_FLOOR:.0%} of baseline "
            f"{base['accuracy']:.1%}).\n"
            f"Cost was reduced by degrading output. Not an improvement."
        )
        return 1

    if cand["p0_missed"] > base["p0_missed"]:
        print(
            f"REJECTED. P0 downgrades rose {base['p0_missed']} -> "
            f"{cand['p0_missed']}. Severity inversion is not a cost win."
        )
        return 1

    ratio = base["cost_per_correct"] / cand["cost_per_correct"]
    delta = 1 - cand["cost_per_correct"] / base["cost_per_correct"]
    saved = base["projected_monthly_usd"] - cand["projected_monthly_usd"]

    print(
        f"cost per correct   ${base['cost_per_correct']:.6f} -> "
        f"${cand['cost_per_correct']:.6f}   ({delta:+.1%}, {ratio:.2f}x)"
    )
    print(
        f"accuracy           {base['accuracy']:.1%} -> {cand['accuracy']:.1%} "
        f"({cand['accuracy'] - base['accuracy']:+.1%})"
    )
    print(f"projected monthly  ${saved:,.0f} saved at {daily_volume():,}/day")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--impl", default="ticket_service")
    ap.add_argument("--compare", nargs=2, metavar=("BASE", "CAND"))
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    tickets = build_corpus()

    if a.compare:
        return compare(a.compare[0], a.compare[1], tickets)

    r = evaluate(a.impl, tickets)
    if a.json:
        print(json.dumps(r, indent=2))
    else:
        print(f"\n{a.impl}")
        print(_fmt(r))
    return 0


if __name__ == "__main__":
    sys.exit(main())
