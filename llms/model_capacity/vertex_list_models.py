#!/usr/bin/env python3
"""
vertex_list_models.py — List all models available in Vertex AI (GCP),
including third-party models like Anthropic Claude, Meta Llama, etc.

Usage:
    python3 vertex_list_models.py --project-id YOUR_PROJECT_ID

Prerequisites:
    1. gcloud auth application-default login
    2. pip install google-cloud-aiplatform
"""

import argparse
import sys
import requests
from google.auth import default as google_auth_default
from google.auth.transport.requests import Request as GoogleAuthRequest

def list_publisher_models(project_id, location="us-central1"):
    """List models available in the Vertex AI Model Garden using confirmed REST API."""
    
    print(f"\n🔍 Querying Vertex AI Model Garden in {location}...")
    
    # Get ADC credentials
    try:
        creds, _ = google_auth_default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
        auth_request = GoogleAuthRequest()
        creds.refresh(auth_request)
        token = creds.token
    except Exception as e:
        print(f"❌ Authentication Error: {e}")
        return

    # Try both regional and global endpoints
    endpoints = [
        f"https://{location}-aiplatform.googleapis.com/v1beta1/publishers/*/models",
        f"https://aiplatform.googleapis.com/v1beta1/publishers/*/models"
    ]
    
    params = {
        "alt": "json",
        "listAllVersions": "True"
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "X-Goog-User-Project": project_id
    }
    
    print(f"{'Source':<10} | {'Publisher':<15} | {'Model ID'}")
    print("-" * 60)

    found_any = False
    for url in endpoints:
        source_label = "region" if f"{location}-" in url else "global"
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code != 200:
                continue
                
            data = response.json()
            models = data.get("publisherModels", [])
            
            if not models:
                # If we get a 200 but no models, check if there's another field name
                if data:
                    print(f"DEBUG [{source_label}]: Received JSON keys: {list(data.keys())}")
                continue

            for model in models:
                found_any = True
                full_name = model.get("name", "")
                parts = full_name.split("/")
                # format: publishers/{pub}/models/{id} or locations/{loc}/publishers/{pub}/models/{id}
                if "publishers" in parts:
                    idx = parts.index("publishers")
                    publisher = parts[idx+1]
                    model_id = parts[idx+3]
                    print(f"{source_label:<10} | {publisher:<15} | {model_id}")

        except Exception as e:
            print(f"DEBUG [{source_label}]: Request failed: {e}")
            continue

    if not found_any:
        print("\n❌ No models found using any standard REST endpoint.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List available Vertex AI models.")
    parser.add_argument("--project-id", required=True, help="Your GCP Project ID")
    parser.add_argument("--location", default="us-central1", help="GCP Region (default: us-central1)")
    args = parser.parse_args()
    
    list_publisher_models(args.project_id, args.location)
