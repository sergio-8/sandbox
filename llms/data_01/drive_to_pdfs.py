import os
import io
import re
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError as GoogleAPIHttpError
from googleapiclient.http import MediaIoBaseDownload
from google.cloud import storage
from google.cloud.exceptions import GoogleCloudError

# --- CONFIGURATION ---
SPREADSHEET_ID = 'ABCD1234567890'
SHEET_RANGE_WITH_URLS = 'Sheet1!A:A'  # <<<< ADAPT THIS (Sheet name, column, header row)
GCS_BUCKET_NAME = 'ABCD1234567890'  # <<<< YOUR TARGET GCS BUCKET

SCOPES = [
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/devstorage.read_write'
]


def authenticate():
    """Handles user authentication for Google APIs."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Failed to refresh token: {e}. Please delete token.json and re-authenticate.")
                creds = None
        if not creds:
            if not os.path.exists('credentials.json'):
                print("Error: 'credentials.json' not found.")
                return None
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def get_urls_from_sheet(creds, spreadsheet_id, range_name):
    """Fetches URLs from a Google Sheet."""
    urls_to_process = []
    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        values = result.get('values', [])
        if not values:
            print('No data found in the specified sheet range.')
            return []
        else:
            # print(f"Found {len(values)} potential rows in the sheet range.") # Less verbose
            for i, row in enumerate(values):
                if row and len(row) > 0 and row[0].strip().startswith('http'):  # Basic URL check
                    url = row[0].strip()
                    urls_to_process.append({'url': url, 'row_number': i + 1})
                    # print(f"Extracted {len(urls_to_process)} valid URLs.")
            return urls_to_process
    except GoogleAPIHttpError as err:
        print(f"An API error occurred while reading the sheet: {err}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred while reading the sheet: {e}")
        return []


def extract_file_id(file_url):
    """
    Extracts the file ID from a Google Drive (Docs, Slides, Sheets) URL.
    Handles URLs like:
    https://docs.google.com/document/d/FILE_ID/edit
    https://docs.google.com/presentation/d/FILE_ID/edit
    https://docs.google.com/file/d/FILE_ID/view
    """
    # Regex to find the ID in common Google Drive URL patterns for Docs and Slides
    # Updated to be more generic for different Google Workspace file types
    match = re.search(r'/(?:document|presentation|spreadsheets|file)/d/([^/]+)', file_url)
    if match:
        return match.group(1)

    # A more general fallback that might catch IDs if the path isn't /d/
    # This is less reliable and might need adjustment based on observed URL patterns.
    # Example: .../folders/FILE_ID or other structures (though less common for direct file links)
    # For now, keeping it focused on /d/ links.

    print(f"Warning: Could not extract a standard File ID from URL: {file_url} using primary patterns.")
    # Fallback attempts (less precise)
    parts = file_url.split('/')
    for i, part in enumerate(parts):
        if part == 'd' and i + 1 < len(parts) and len(parts[i + 1]) > 30:  # Check for '/d/LONG_ID'
            potential_id = parts[i + 1].split('?')[0].split('#')[0]  # Clean query params
            if len(potential_id) > 30:  # Re-check length after cleaning
                print(f"  Fallback attempt extracted: {potential_id}")
                return potential_id
    return None


def export_file_and_upload_to_gcs(creds, file_url, gcs_bucket_name, gcs_blob_name):
    """Exports a Google Drive file (Doc or Slide) to PDF and uploads it to GCS."""
    try:
        drive_service = build('drive', 'v3', credentials=creds)
        file_id = extract_file_id(file_url)  # Use the updated function

        if not file_id:
            print(f"Skipping URL due to missing or unextractable file ID: {file_url}")
            return False

        print(f"  Attempting to export File ID: {file_id} (from URL: {file_url})")
        request = drive_service.files().export_media(fileId=file_id, mimeType='application/pdf')

        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        print(f"  Downloading PDF to memory for '{gcs_blob_name}'...", end='')
        while done is False:
            status, done = downloader.next_chunk()
            if status:
                print(f'\r  Downloading PDF to memory for \'{gcs_blob_name}\'... {int(status.progress() * 100)}%.',
                      end='')
        print(f"\r  Downloading PDF to memory for '{gcs_blob_name}'... Complete.     ")

        fh.seek(0)

        storage_client = storage.Client(credentials=creds)
        bucket = storage_client.bucket(gcs_bucket_name)
        blob = bucket.blob(gcs_blob_name)

        print(f"  Uploading to GCS: gs://{gcs_bucket_name}/{gcs_blob_name}...")
        blob.upload_from_file(fh, content_type='application/pdf')
        fh.close()
        print(f"  Successfully uploaded to gs://{gcs_bucket_name}/{gcs_blob_name}")
        return True

    except GoogleAPIHttpError as error:
        print(f'\n  A Google API error occurred for {file_url}: {error}')
        print(f'  Details: {error.resp.status} - {error._get_reason()}')
        if error.resp.status == 404:
            print(
                f"  Error 404: File (ID: {file_id if 'file_id' in locals() else 'unknown'}) not found. Check ID and permissions.")
        elif error.resp.status == 403:
            print(
                f"  Error 403: Permission denied for File (ID: {file_id if 'file_id' in locals() else 'unknown'}). Check access and Drive API.")
        return False
    except GoogleCloudError as e:
        print(
            f"\n  A Google Cloud Storage error occurred for {file_url} -> gs://{gcs_bucket_name}/{gcs_blob_name}: {e}")
        if hasattr(e, 'code') and e.code == 403:
            print(f"  GCS Error 403: Permission denied for bucket '{gcs_bucket_name}'. Check IAM permissions.")
        elif hasattr(e, 'code') and e.code == 404:
            print(f"  GCS Error 404: Bucket '{gcs_bucket_name}' not found.")
        return False
    except Exception as e:
        print(f"\n  An unexpected error occurred for {file_url}: {e}")
        return False


if __name__ == '__main__':
    print("Starting batch PDF conversion and GCS upload process...")

    creds = authenticate()

    if not creds:
        print("Authentication failed. Cannot proceed.")
    else:
        print(
            f"Successfully authenticated. Reading URLs from Google Sheet ID: {SPREADSHEET_ID}, Range: {SHEET_RANGE_WITH_URLS}")
        urls_to_process = get_urls_from_sheet(creds, SPREADSHEET_ID, SHEET_RANGE_WITH_URLS)

        if not urls_to_process:
            print("No URLs found in the Google Sheet or unable to read them. Exiting.")
        else:
            print(f"\nFound {len(urls_to_process)} URLs to process from the sheet.")
            successful_uploads = 0
            failed_uploads = 0

            for index, url_info in enumerate(urls_to_process):
                url = url_info['url']
                row_num = url_info['row_number']

                print(f"\nProcessing URL #{index + 1} (from sheet row {row_num}): {url}")

                # Generate a GCS object name
                file_id_for_name = extract_file_id(url)  # Use updated function here too for consistent naming
                if file_id_for_name:
                    safe_id_part = re.sub(r'[^a-zA-Z0-9_-]', '', file_id_for_name)
                    # Consider making the prefix generic, e.g., "file_" instead of "presentation_"
                    gcs_object_name = f"file_{safe_id_part}_row{row_num}.pdf"
                else:
                    gcs_object_name = f"file_export_row{row_num}_{index + 1}.pdf"
                    print(
                        f"  Using fallback GCS object name: {gcs_object_name} (due to ID extraction issue for naming)")

                if export_file_and_upload_to_gcs(creds, url, GCS_BUCKET_NAME, gcs_object_name):
                    successful_uploads += 1
                else:
                    failed_uploads += 1

            print(f"\n--- Batch Processing Complete ---")
            print(f"Successfully exported and uploaded to GCS: {successful_uploads}")
            print(f"Failed attempts: {failed_uploads}")

    print("\nScript finished.")