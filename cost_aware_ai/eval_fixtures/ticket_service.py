"""Support ticket triage service.

Classifies inbound support tickets into one of twelve categories and assigns
a priority. Currently handling ~50,000 tickets/day, growing about 15% month
over month.

Owner: support-platform@
"""

from __future__ import annotations

import datetime
import json
import re

from corpus import CATEGORIES
from fake_model import FakeModel

# --------------------------------------------------------------------------
# Static instructions. ~6,000 tokens of category definitions, escalation
# policy, tone guidance and worked examples. Identical on every request.
# --------------------------------------------------------------------------

CATEGORY_GUIDE = "\n".join(
    f"{c}: Assign when the customer's primary intent matches {c.lower().replace('_', ' ')}. "
    f"Consider tone, urgency, prior history and the specific remedy requested. "
    f"Do not assign when another category fits more precisely. "
    f"Worked example: a customer describing {c.lower().replace('_', ' ')} in "
    f"passing while asking about something else belongs in the other category. " * 12
    for c in CATEGORIES
)

ESCALATION_POLICY = (
    "Escalation policy: P0 pages the on-call within five minutes. P1 enters "
    "the priority queue with a four hour SLA. P2 is next business day. P3 is "
    "best effort. Do not assign P0 unless there is active financial or "
    "security exposure. " * 40
)

STATIC_PREFIX = f"""You are a support triage assistant.

{CATEGORY_GUIDE}

{ESCALATION_POLICY}
"""

# --------------------------------------------------------------------------
# Tool registry. Every schema is sent on every request.
# --------------------------------------------------------------------------

TOOL_NAMES = [
    "lookup_order",
    "lookup_account",
    "lookup_invoice",
    "issue_refund",
    "cancel_subscription",
    "reset_password",
    "lock_account",
    "unlock_account",
    "create_rma",
    "check_warranty",
    "escalate_to_human",
    "send_email",
    "send_sms",
    "update_address",
    "apply_credit",
    "check_shipment",
    "reorder_item",
    "check_stock",
    "flag_fraud",
    "freeze_card",
    "verify_identity",
    "log_security_event",
    "open_dispute",
    "close_dispute",
    "fetch_transcript",
    "search_kb",
    "create_followup",
    "snooze_ticket",
    "merge_tickets",
    "split_ticket",
    "tag_ticket",
    "assign_agent",
    "check_sla",
    "extend_sla",
    "notify_manager",
    "record_csat",
    "translate_text",
    "detect_language",
    "summarize_thread",
    "list_devices",
    "check_firmware",
    "push_update",
    "schedule_callback",
    "cancel_callback",
    "check_balance",
    "add_payment_method",
    "remove_payment_method",
    "update_plan",
    "pause_subscription",
    "resume_subscription",
    "gift_credit",
    "check_promo",
    "apply_promo",
    "validate_coupon",
    "check_eligibility",
    "start_trial",
    "end_trial",
    "export_data",
    "delete_account",
    "restore_account",
    "check_consent",
    "update_consent",
]

TOOL_SCHEMAS = [
    {
        "name": n,
        "description": (
            f"Invoke the {n.replace('_', ' ')} operation for a customer. "
            f"Accepts an identifier and optional parameters. Returns a status "
            f"object with the outcome and any resulting state change. "
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "Target identifier."},
                "reason": {"type": "string", "description": "Audit reason."},
                "amount": {"type": "number", "description": "Optional amount."},
            },
            "required": ["id"],
        },
    }
    for n in TOOL_NAMES
]


def build_prompt(ticket) -> str:
    """Assemble the request sent to the model."""
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return (
        f"Request timestamp: {now}\n"
        f"Request id: {ticket.id}-{now}\n"
        f"{STATIC_PREFIX}\n"
        f"AVAILABLE_TOOLS:\n{json.dumps(TOOL_SCHEMAS)}\n\n"
        f"Think step by step and explain your reasoning in full before "
        f"stating your conclusion.\n\n"
        f"TICKET: {ticket.text}\n"
    )


def parse_response(text: str) -> tuple[str, str]:
    """Extract the category and priority from the model's prose."""
    cat = "GENERAL_INQUIRY"
    for c in ("BILLING_QUESTION", "SHIPPING_DELAY", "PASSWORD_RESET"):
        if c in text:
            cat = c
            break
    m = re.search(r"\bP([0-3])\b", text)
    prio = f"P{m.group(1)}" if m else "P3"
    return cat, prio


def classify(ticket, model: FakeModel) -> tuple[str, str]:
    """Classify one ticket."""
    prompt = build_prompt(ticket)

    attempts = 0
    while True:
        attempts += 1
        text, _ = model.generate(
            prompt, model="pro", ticket=ticket, path="classify"
        )
        cat, prio = parse_response(text)
        if cat in CATEGORIES:
            return cat, prio
        # Retry until the parser is satisfied.
        if attempts > 6:
            return "GENERAL_INQUIRY", "P3"


def nightly_summary(tickets, model: FakeModel) -> list[str]:
    """Produce a one-line summary of each ticket for the morning report."""
    out = []
    for t in tickets:
        text, _ = model.generate(
            f"{STATIC_PREFIX}\nSummarize in one line: {t.text}",
            model="pro",
            path="nightly",
        )
        out.append(text)
    return out


def run(tickets, model: FakeModel) -> dict[str, tuple[str, str]]:
    """Process a batch of tickets, then build the morning report."""
    results = {}
    for t in tickets:
        results[t.id] = classify(t, model)
    nightly_summary(tickets, model)
    return results
