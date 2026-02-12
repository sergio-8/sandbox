#!/usr/bin/env python3
"""
Downloads files and folders from Google Drive using Application Default Credentials (ADC).
Converts Google Docs/Slides/Sheets to PDF.
"""

import argparse
import io
import os
import re
from typing import List, Optional

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

# Scopes required for read-only access to Drive
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# MIME Types for conversion
EXPORT_MIME_TYPES = {
    'application/vnd.google-apps.document': ('application/pdf', '.pdf'),
    'application/vnd.google-apps.presentation': ('application/pdf', '.pdf'),
    'application/vnd.google-apps.spreadsheet': ('application/pdf', '.pdf'),
}

def extract_id(url_or_id: str) -> str:
    """Extracts ID from URL or returns ID as is."""
    patterns = [
        r'/file/d/([a-zA-Z0-9_-]+)',
        r'/document/d/([a-zA-Z0-9_-]+)',
        r'/spreadsheets/d/([a-zA-Z0-9_-]+)',
        r'/presentation/d/([a-zA-Z0-9_-]+)',
        r'/folders/([a-zA-Z0-9_-]+)',
        r'id=([a-zA-Z0-9_-]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    return url_or_id

def download_file(service, file_id: str, file_name: str, mime_type: str, output_path: str):
    """Downloads a single file or exports a Google Doc to PDF."""
    try:
        if mime_type in EXPORT_MIME_TYPES:
            export_mime, ext = EXPORT_MIME_TYPES[mime_type]
            if not file_name.endswith(ext):
                file_name += ext
            request = service.files().export_media(fileId=file_id, mimeType=export_mime)
        else:
            request = service.files().get_media(fileId=file_id)

        file_path = os.path.join(output_path, file_name)
        fh = io.FileIO(file_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        print(f"Downloading {file_name}...", end='\r')
        while done is False:
            status, done = downloader.next_chunk()
        print(f"✓ Downloaded {file_name} ")
    except HttpError as error:
        print(f"✗ Failed to download {file_name}: {error}")

def process_item(service, item_id: str, output_path: str):
    """Processes either a folder or a file."""
    try:
        print(f"🔍 Checking ID: {item_id}")
        item = service.files().get(fileId=item_id, fields='id, name, mimeType', supportsAllDrives=True).execute()
        name = item.get('name')
        mime_type = item.get('mimeType')
        print(f"   Found: {name} ({mime_type})")

        if mime_type == 'application/vnd.google-apps.folder':
            print(f"📂 Entering folder: {name}")
            folder_path = os.path.join(output_path, name)
            os.makedirs(folder_path, exist_ok=True)
            
            results = service.files().list(
                q=f"'{item_id}' in parents and trashed = false",
                fields="nextPageToken, files(id, name, mimeType)",
                supportsAllDrives=True,
                includeItemsFromAllDrives=True
            ).execute()
            
            items = results.get('files', [])
            print(f"   Folder contains {len(items)} items.")
            for child in items:
                process_item(service, child['id'], folder_path)
        else:
            download_file(service, item_id, name, mime_type, output_path)

    except HttpError as error:
        print(f"✗ Error processing {item_id}: {error.resp.status} {error.reason}")

def main():
    parser = argparse.ArgumentParser(description="Download Google Drive files/folders using ADC.")
    parser.add_argument("--id", required=True, help="Google Drive File/Folder ID or URL")
    parser.add_argument("--output", default="./drive_downloads", help="Local directory to save files")
    parser.add_argument("--project", help="GCP Project ID to use for API quota (e.g. sv-ml-sandbox)")
    args = parser.parse_args()

    # 1. Authenticate with ADC
    try:
        print("Authenticating with Application Default Credentials...")
        
        # Explicitly set the ADC path to avoid GCE metadata server interference
        adc_path = os.path.expanduser("~/.config/gcloud/application_default_credentials.json")
        if os.path.exists(adc_path):
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = adc_path
            print(f"  - Forced credentials path: {adc_path}")

        creds, discovered_project = google.auth.default(scopes=SCOPES)
        
        # If user provided a project, force it as the quota project
        project = args.project or discovered_project
        if args.project and hasattr(creds, 'with_quota_project'):
            creds = creds.with_quota_project(args.project)
            print(f"  - Forced quota project: {args.project}")
        
        if not creds:
             raise Exception("No credentials found. Please run 'gcloud auth application-default login'.")
        
        # Verbose credential info
        print(f"  - Credential Type: {type(creds).__name__}")
        print(f"  - Account: {getattr(creds, 'service_account_email', getattr(creds, 'account', 'Unknown'))}")
        print(f"  - Project: {project}")
        
        service = build('drive', 'v3', credentials=creds)
    except Exception as e:
        print(f"✗ Authentication failed: {e}")
        print("\nPlease run this in your personal terminal first:")
        print("gcloud auth application-default login --scopes='https://www.googleapis.com/auth/drive.readonly,https://www.googleapis.com/auth/cloud-platform'")
        return

    # 2. Extract ID and Start Processing
    item_id = extract_id(args.id)
    os.makedirs(args.output, exist_ok=True)
    
    print(f"\nStarting download of ID: {item_id} into {args.output}\n")
    process_item(service, item_id, args.output)
    print("\n✨ Done!")

if __name__ == "__main__":
    main()
