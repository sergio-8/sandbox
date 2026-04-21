#!/usr/bin/env python3
"""
list_models.py — A simple script to list all Gemini models available via your API key.

Usage:
    python3 list_models.py --api-key YOUR_API_KEY
"""

import argparse
import requests
import sys

def list_models(api_key):
    url = "https://generativelanguage.googleapis.com/v1beta/models"
    params = {"key": api_key}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        models = data.get("models", [])
        
        if not models:
            print("No models found.")
            return

        print(f"\n{'Model Name':<40} | {'Supported Methods'}")
        print("-" * 75)
        
        for model in models:
            name = model.get("name", "").replace("models/", "")
            methods = ", ".join(model.get("supportedGenerationMethods", []))
            print(f"{name:<40} | {methods}")
            
        print(f"\nTotal models found: {len(models)}\n")

    except requests.exceptions.HTTPError as err:
        print(f"❌ HTTP Error: {err}")
        if response.status_code == 401:
            print("   Check if your API key is valid.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List available Gemini models.")
    parser.add_argument("--api-key", required=True, help="Your Gemini API key")
    args = parser.parse_args()
    
    list_models(args.api_key)
