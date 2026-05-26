#!/usr/bin/env python3
"""
quota_check.py — List remaining free-tier daily quota for each Gemini model.

Usage:
    python quota_check.py --project-id YOUR_PROJECT_ID --api-key YOUR_API_KEY

Requirements:
    pip install requests google-auth google-cloud-monitoring

How it works:
  1. Lists available Gemini models via the Generative Language REST API (API key).
  2. Queries Cloud Monitoring for the last 24 h of free-tier quota usage per model.
  3. Fetches quota limits from the Cloud Quotas API (uses Application Default Credentials).
  4. Prints a table: Model | Daily Limit | Used (24 h) | Remaining.

Authentication note:
  Cloud Monitoring and Cloud Quotas require GCP credentials beyond a plain API key.
  Run `gcloud auth application-default login` once, or set GOOGLE_APPLICATION_CREDENTIALS
  to a service account JSON.  The --api-key flag is only used for the Gemini model list.
"""

import argparse
import sys
from datetime import datetime, timedelta, timezone

import requests
from google.auth import default as google_auth_default
from google.auth.transport.requests import Request as GoogleAuthRequest
from google.cloud import monitoring_v3

# ── Constants ────────────────────────────────────────────────────────────────
GEMINI_LIST_MODELS_URL = "https://generativelanguage.googleapis.com/v1beta/models"
CLOUD_QUOTAS_API = (
    "https://cloudquotas.googleapis.com/v1/projects/{project_id}/locations/global"
    "/services/generativelanguage.googleapis.com/quotaInfos"
)
FREE_TIER_METRIC_PREFIX = "generate_content_free_tier_requests"


# ── Step 1: List Gemini models ───────────────────────────────────────────────

def list_gemini_models(api_key: str) -> list[str]:
    """Return a sorted list of model IDs available for the given API key."""
    resp = requests.get(GEMINI_LIST_MODELS_URL, params={"key": api_key}, timeout=10)
    resp.raise_for_status()
    models = resp.json().get("models", [])
    # model name looks like "models/gemini-2.0-flash" → strip prefix
    return sorted(m["name"].replace("models/", "") for m in models)


# ── Step 2: Get GCP credentials for Cloud APIs ──────────────────────────────

def get_gcp_credentials():
    """Return (credentials, project) using Application Default Credentials."""
    creds, project = google_auth_default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    creds.refresh(GoogleAuthRequest())
    return creds


# ── Step 3: Query Cloud Monitoring for free-tier usage in the last 24 h ─────

def get_quota_usage(project_id: str, creds) -> dict[str, int]:
    """
    Query Cloud Monitoring for free-tier request usage per model in the last 24 h.
    Returns a dict: {model_id: total_requests_in_24h}.
    """
    client = monitoring_v3.MetricServiceClient(credentials=creds)
    project_name = f"projects/{project_id}"

    now = datetime.now(tz=timezone.utc)
    interval = monitoring_v3.TimeInterval(
        start_time=now - timedelta(hours=24),
        end_time=now,
    )

    # Quota usage metric (free tier)
    metric_filter = (
        'metric.type="serviceruntime.googleapis.com/quota/rate/net_usage" '
        'AND resource.type="consumer_quota" '
        f'AND resource.labels.service="generativelanguage.googleapis.com" '
        f'AND metric.labels.quota_metric=~".*free_tier_requests.*"'
    )

    usage: dict[str, int] = {}
    try:
        results = client.list_time_series(
            request={
                "name": project_name,
                "filter": metric_filter,
                "interval": interval,
                "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            }
        )
        for ts in results:
            model_label = ts.metric.labels.get("model", "unknown")
            total = sum(p.value.int64_value for p in ts.points)
            usage[model_label] = usage.get(model_label, 0) + total
    except Exception as exc:  # pylint: disable=broad-except
        print(f"  ⚠️  Could not fetch usage from Cloud Monitoring: {exc}", file=sys.stderr)

    return usage


# ── Step 4: Fetch free-tier quota limits from Cloud Quotas API ──────────────

def get_quota_limits(project_id: str, creds) -> dict[str, int]:
    """
    Call the Cloud Quotas API to get per-model free-tier daily request limits.
    Returns a dict: {model_id: daily_limit}.
    """
    url = CLOUD_QUOTAS_API.format(project_id=project_id)
    headers = {"Authorization": f"Bearer {creds.token}"}
    limits: dict[str, int] = {}

    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        for qi in resp.json().get("quotaInfos", []):
            metric = qi.get("quotaMetric", "")
            if "free_tier_requests" not in metric:
                continue
            for pb in qi.get("quotaPreferences", []) + qi.get("quotaBuckets", []):
                dimensions = pb.get("dimensions", {})
                model = dimensions.get("model", "")
                # effectiveLimit holds the actual enforced limit
                effective = pb.get("effectiveLimit", {}).get("value")
                if model and effective is not None:
                    limits[model] = int(effective)
    except Exception as exc:  # pylint: disable=broad-except
        print(f"  ⚠️  Could not fetch limits from Cloud Quotas API: {exc}", file=sys.stderr)
        print(
            "     (Tip: ensure the Cloud Quotas API is enabled and "
            "you have `roles/serviceusage.serviceUsageViewer`)",
            file=sys.stderr,
        )

    return limits


# ── Step 5: Print summary table ──────────────────────────────────────────────

def print_table(models: list[str], limits: dict[str, int], usage: dict[str, int]) -> None:
    COL = [42, 14, 14, 14]
    header = ["Model", "Daily Limit", "Used (24h)", "Remaining"]
    sep = "─" * (sum(COL) + 3 * 3 + 2)

    print()
    print(sep)
    print(
        f" {header[0]:<{COL[0]}} │ {header[1]:>{COL[1]}} │ {header[2]:>{COL[2]}} │ {header[3]:>{COL[3]}}"
    )
    print(sep)

    for model in models:
        limit = limits.get(model)
        used = usage.get(model, 0)

        if limit is None:
            limit_str = "n/a"
            remaining_str = "n/a"
        else:
            remaining = max(0, limit - used)
            limit_str = f"{limit:,}"
            remaining_str = f"{remaining:,}"
            if remaining == 0:
                remaining_str = "🔴 EXHAUSTED"
            elif remaining < limit * 0.1:
                remaining_str = f"🟡 {remaining:,}"
            else:
                remaining_str = f"🟢 {remaining:,}"

        used_str = f"{used:,}" if used else "—"
        print(
            f" {model:<{COL[0]}} │ {limit_str:>{COL[1]}} │ {used_str:>{COL[2]}} │ {remaining_str:>{COL[3]}}"
        )

    print(sep)
    print(
        f"\n Checked at: {datetime.now(tz=timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}\n"
    )


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Show remaining free-tier daily quota for each Gemini model.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--project-id", required=True, help="GCP project ID")
    parser.add_argument("--api-key", required=True, help="Gemini API key (for model list)")
    parser.add_argument(
        "--skip-monitoring",
        action="store_true",
        help="Skip Cloud Monitoring (show limits only, usage will show as —)",
    )
    args = parser.parse_args()

    # 1 — List models
    print(f"\n🔍 Fetching available Gemini models …")
    try:
        models = list_gemini_models(args.api_key)
        print(f"   Found {len(models)} models.")
    except Exception as exc:
        print(f"❌ Failed to list models: {exc}", file=sys.stderr)
        sys.exit(1)

    # 2 — GCP credentials (ADC)
    print("🔑 Loading GCP credentials (Application Default Credentials) …")
    try:
        creds = get_gcp_credentials()
    except Exception as exc:
        print(f"❌ GCP credentials error: {exc}", file=sys.stderr)
        print("   Run: gcloud auth application-default login", file=sys.stderr)
        sys.exit(1)

    # 3 — Quota limits
    print("📋 Fetching quota limits from Cloud Quotas API …")
    limits = get_quota_limits(args.project_id, creds)

    # 4 — Quota usage
    if args.skip_monitoring:
        usage: dict[str, int] = {}
    else:
        print("📊 Fetching 24 h usage from Cloud Monitoring …")
        usage = get_quota_usage(args.project_id, creds)

    # 5 — Print table
    print_table(models, limits, usage)

    # 6 — Final Advice
    if not limits or not usage:
        print("\n💡 Tip: Since some APIs are restricted, you can also see your real-time usage here:")
        print(f"   👉 https://aistudio.google.com/app/plan")
        if not usage:
            print("\n   Note: Cloud Monitoring (used for 'Used' column) REQUIRES billing to be enabled on your GCP project.")
