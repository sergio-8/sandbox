"""Synthetic support-ticket corpus with ground-truth labels.

Generates 150 tickets, deterministically seeded. Correctness of any classifier
run against this corpus is decided by exact match against `label_category`,
so grading requires no model and no human.

Composition is deliberate:

  90  easy       unambiguous from surface text alone
  30  hard       require `account_context`; text alone is insufficient
  30  collision  15 pairs of *byte-identical* text carrying opposite labels

The collision set is the load-bearing part. Because the two members of a pair
are identical strings, any classifier that decides from surface form alone
cannot exceed 50% on that subset. That is a property of the data, not of the
simulation -- it is the mechanical statement of "difficulty is often not
visible in wording".
"""

from __future__ import annotations

import dataclasses
import random

SEED = 20260803

CATEGORIES = (
    "BILLING_QUESTION",
    "BILLING_DISPUTE",
    "FRAUD_REPORT",
    "ACCOUNT_ACCESS",
    "PASSWORD_RESET",
    "SHIPPING_DELAY",
    "RETURN_REQUEST",
    "PRODUCT_DEFECT",
    "FEATURE_REQUEST",
    "SECURITY_CONCERN",
    "CANCELLATION",
    "GENERAL_INQUIRY",
)

# Business rule: category implies a priority band. A prediction that pairs a
# category with a priority outside its band is *structurally invalid* and can
# be rejected without knowing the right answer. This is what makes a
# deterministic verifier possible (technique 5).
PRIORITY_BAND = {
    "FRAUD_REPORT": {"P0", "P1"},
    "SECURITY_CONCERN": {"P0", "P1"},
    "ACCOUNT_ACCESS": {"P1", "P2"},
    "BILLING_DISPUTE": {"P1", "P2"},
    "PRODUCT_DEFECT": {"P1", "P2"},
    "SHIPPING_DELAY": {"P2", "P3"},
    "RETURN_REQUEST": {"P2", "P3"},
    "CANCELLATION": {"P2", "P3"},
    "PASSWORD_RESET": {"P2", "P3"},
    "BILLING_QUESTION": {"P2", "P3"},
    "FEATURE_REQUEST": {"P3"},
    "GENERAL_INQUIRY": {"P3"},
}


@dataclasses.dataclass(frozen=True)
class Ticket:
    """One inbound ticket plus its ground truth."""

    id: str
    text: str
    # Retrievable state. Not present in `text`. An implementation must choose
    # to look this up; the naive service never does.
    account_context: dict
    label_category: str
    label_priority: str
    difficulty: str  # "easy" | "hard"
    collision_group: str | None  # non-None => text is shared with a sibling


# --- easy: one distinctive template per category --------------------------

_EASY_TEMPLATES = {
    "BILLING_QUESTION": "Can you explain the ${amt} line item on invoice {inv}?",
    "BILLING_DISPUTE": "I was charged ${amt} twice on invoice {inv}. Refund one.",
    "FRAUD_REPORT": "There is a ${amt} charge from a store I have never used.",
    "ACCOUNT_ACCESS": "My account is locked out after too many attempts.",
    "PASSWORD_RESET": "The password reset email never arrives. Please resend.",
    "SHIPPING_DELAY": "Order {inv} has said 'in transit' for eleven days.",
    "RETURN_REQUEST": "I would like to return order {inv}, wrong size.",
    "PRODUCT_DEFECT": "The hinge on the unit from order {inv} snapped in week two.",
    "FEATURE_REQUEST": "Please add CSV export to the reporting dashboard.",
    "SECURITY_CONCERN": "I received a 2FA prompt I did not initiate, twice.",
    "CANCELLATION": "Cancel my subscription at the end of the billing period.",
    "GENERAL_INQUIRY": "What are your customer support hours on weekends?",
}

_EASY_PRIORITY = {
    "BILLING_QUESTION": "P3",
    "BILLING_DISPUTE": "P2",
    "FRAUD_REPORT": "P0",
    "ACCOUNT_ACCESS": "P2",
    "PASSWORD_RESET": "P3",
    "SHIPPING_DELAY": "P3",
    "RETURN_REQUEST": "P3",
    "PRODUCT_DEFECT": "P2",
    "FEATURE_REQUEST": "P3",
    "SECURITY_CONCERN": "P1",
    "CANCELLATION": "P2",
    "GENERAL_INQUIRY": "P3",
}

# --- hard: resolvable, but only from account_context ----------------------

_HARD_TEMPLATES = (
    (
        "This is the third time I am writing about order {inv}.",
        # discriminated by prior_contacts and order state
        ("SHIPPING_DELAY", "P2"),
        ("PRODUCT_DEFECT", "P1"),
    ),
    (
        "I need this resolved before my renewal date.",
        ("CANCELLATION", "P2"),
        ("BILLING_DISPUTE", "P1"),
    ),
    (
        "Something looks wrong with my account activity.",
        ("SECURITY_CONCERN", "P1"),
        ("BILLING_QUESTION", "P3"),
    ),
)

# --- collisions: identical text, opposite label ---------------------------
# Each entry: (shared_text, (ctx_a, label_a, prio_a), (ctx_b, label_b, prio_b))

_COLLISIONS = (
    (
        "Where is this charge from? I do not recognise it.",
        (
            {"recent_order_matches_charge": True, "geo_anomaly": False},
            "BILLING_QUESTION",
            "P3",
        ),
        (
            {"recent_order_matches_charge": False, "geo_anomaly": True},
            "FRAUD_REPORT",
            "P0",
        ),
    ),
    (
        "I cannot log in to my account.",
        ({"failed_logins_24h": 3, "new_country_login": False}, "PASSWORD_RESET", "P3"),
        (
            {"failed_logins_24h": 41, "new_country_login": True},
            "SECURITY_CONCERN",
            "P0",
        ),
    ),
    (
        "My package never arrived.",
        (
            {"carrier_status": "IN_TRANSIT", "address_changed_recently": False},
            "SHIPPING_DELAY",
            "P2",
        ),
        (
            {"carrier_status": "DELIVERED", "address_changed_recently": True},
            "FRAUD_REPORT",
            "P0",
        ),
    ),
    (
        "I want to stop being billed for this.",
        (
            {"subscription_active": True, "disputed_charges_90d": 0},
            "CANCELLATION",
            "P2",
        ),
        (
            {"subscription_active": False, "disputed_charges_90d": 4},
            "BILLING_DISPUTE",
            "P1",
        ),
    ),
    (
        "The device stopped working after the update.",
        (
            {"warranty_active": True, "known_firmware_issue": True},
            "PRODUCT_DEFECT",
            "P1",
        ),
        (
            {"warranty_active": False, "known_firmware_issue": False},
            "GENERAL_INQUIRY",
            "P3",
        ),
    ),
)


def _pad_context(rng: random.Random, base: dict) -> dict:
    """Add stable filler so context size does not itself leak the label."""
    ctx = dict(base)
    ctx.setdefault("tenure_months", rng.randint(1, 96))
    ctx.setdefault("lifetime_value_band", rng.choice(["low", "mid", "high"]))
    ctx.setdefault("prior_contacts_30d", rng.randint(0, 6))
    return ctx


def build_corpus(n_easy: int = 90, n_hard: int = 30, n_collision_pairs: int = 15):
    """Return a deterministic list of 150 tickets (default sizing)."""
    rng = random.Random(SEED)
    tickets: list[Ticket] = []
    i = 0

    for k in range(n_easy):
        cat = CATEGORIES[k % len(CATEGORIES)]
        text = _EASY_TEMPLATES[cat].format(
            amt=rng.randint(9, 480), inv=f"A{rng.randint(10000, 99999)}"
        )
        tickets.append(
            Ticket(
                id=f"T{i:04d}",
                text=text,
                account_context=_pad_context(rng, {}),
                label_category=cat,
                label_priority=_EASY_PRIORITY[cat],
                difficulty="easy",
                collision_group=None,
            )
        )
        i += 1

    for k in range(n_hard):
        text_tpl, (cat_a, pa), (cat_b, pb) = _HARD_TEMPLATES[k % len(_HARD_TEMPLATES)]
        take_a = k % 2 == 0
        cat, prio = (cat_a, pa) if take_a else (cat_b, pb)
        tickets.append(
            Ticket(
                id=f"T{i:04d}",
                text=text_tpl.format(inv=f"A{rng.randint(10000, 99999)}"),
                account_context=_pad_context(
                    rng, {"escalation_history": not take_a, "open_rma": not take_a}
                ),
                label_category=cat,
                label_priority=prio,
                difficulty="hard",
                collision_group=None,
            )
        )
        i += 1

    for k in range(n_collision_pairs):
        text, (ctx_a, cat_a, pa), (ctx_b, cat_b, pb) = _COLLISIONS[k % len(_COLLISIONS)]
        group = f"C{k:02d}"
        for ctx, cat, prio in ((ctx_a, cat_a, pa), (ctx_b, cat_b, pb)):
            tickets.append(
                Ticket(
                    id=f"T{i:04d}",
                    text=text,  # byte-identical across the pair, by design
                    account_context=_pad_context(rng, ctx),
                    label_category=cat,
                    label_priority=prio,
                    difficulty="hard",
                    collision_group=group,
                )
            )
            i += 1

    return tickets


def daily_volume() -> int:
    """Production volume the fixture represents. Corpus is a 0.3% sample."""
    return 50_000


if __name__ == "__main__":
    c = build_corpus()
    print(f"{len(c)} tickets")
    for d in ("easy", "hard"):
        print(f"  {d:9s} {sum(1 for t in c if t.difficulty == d)}")
    print(f"  collision {sum(1 for t in c if t.collision_group)}")
