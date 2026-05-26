#!/usr/bin/env python3
"""
claude_vertex_test.py — Simple test to invoke claude-opus-4-7 via Vertex AI (Google Cloud).

Usage:
    python3 claude_vertex_test.py --project-id YOUR_PROJECT_ID

Prerequisites:
    1. gcloud auth application-default login
    2. pip install 'anthropic[vertex]'
"""

import argparse

MODEL_ID = "claude-opus-4-7"

def run_test(project_id: str, location: str = "global"):
    try:
        import anthropic
    except ImportError:
        print("❌ Missing dependency. Run: pip install 'anthropic[vertex]'")
        return

    client = anthropic.AnthropicVertex(project_id=project_id, region=location)

    print(f"\n🤖 Calling {MODEL_ID} via Vertex AI (project={project_id}, region={location})...")

    try:
        message = client.messages.create(
            model=MODEL_ID,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": "Say hello and tell me one fun fact about the ocean."},
            ],
        )
        print("\n✅ Response received!")
        print("-" * 60)
        print(message.content[0].text)
        print("-" * 60)
        print(f"\nUsage → input_tokens: {message.usage.input_tokens}, output_tokens: {message.usage.output_tokens}")

    except Exception as e:
        print(f"❌ Failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test Claude on Vertex AI.")
    parser.add_argument("--project-id", required=True, help="Your GCP Project ID")
    parser.add_argument("--location", default="global", help="Vertex AI region (default: global)")
    args = parser.parse_args()

    run_test(args.project_id, args.location)
