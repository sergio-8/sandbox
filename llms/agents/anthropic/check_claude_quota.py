#!/usr/bin/env python3
"""
check_claude_quota.py — Check your Vertex AI quota for Claude 4.7.
"""

import argparse
import requests
import json
from google.auth import default as google_auth_default
from google.auth.transport.requests import Request as GoogleAuthRequest

def get_quota(project_id, location="us-east5"):
    print(f"🔍 Checking Claude quota for project: {project_id} in {location}...")
    
    # Get ADC credentials
    try:
        creds, _ = google_auth_default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
        auth_request = GoogleAuthRequest()
        creds.refresh(auth_request)
        token = creds.token
    except Exception as e:
        print(f"❌ Authentication Error: {e}")
        return

    # Use the Cloud Quotas API
    # The quota ID for Vertex AI online prediction is typically 'OnlinePredictionRequestsPerModelPerProjectPerRegion'
    # We query the details for this specific project and location.
    
    url = f"https://cloudquotas.googleapis.com/v1/projects/{project_id}/locations/{location}/quotaInfos"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "X-Goog-User-Project": project_id
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        quota_infos = data.get("quotaInfos", [])
        
        found = False
        print(f"\n{'Quota Name':<60} | {'Limit'} | {'Usage'}")
        print("-" * 80)
        
        # Search for online prediction and token-specific quotas
        search_terms = ["online_prediction", "anthropic", "tokens", "requests"]
        
        for info in quota_infos:
            name = info.get("name", "").split("/")[-1].lower()
            if any(term in name for term in search_terms):
                found = True
                limit = info.get("quotaValue", "N/A")
                metric = info.get("metric", "N/A")
                print(f"{name[:60]:<60} | {limit:<7} | {metric}")

        if not found:
            print("❌ No Claude-specific quotas found in this region.")
            print("💡 Tip: Quotas migrate to 'active' once the model is first invoked successfully.")

    except Exception as e:
        print(f"❌ Error: {e}")
        if "403" in str(e):
            print("\n💡 Your account might need the 'Cloud Quotas Viewer' role.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--location", default="us-east5")
    args = parser.parse_args()
    
    get_quota(args.project_id, args.location)
