# This script analyzes the sharing permissions of Google Docs listed in a Google Sheet.
# It categorizes them based on domain-level view access and writes the file names
# back to specific tabs in the same spreadsheet.

import os.path
import re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# --- CONFIGURATION ---
# IMPORTANT: If you change the scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.readonly",
]

# The ID of your Google Spreadsheet.
# Extracted from your URL: https://docs.google.com/spreadsheets/d/1xopRuweCz4KBmTGjLTOVO3krE2kjJBGUXXuBBH1lfsk/edit
SPREADSHEET_ID = "1xopRuweCz4KBmTGjLTOVO3krE2kjJBGUXXuBBH1lfsk"

# Names of the tabs (worksheets) in your spreadsheet.
SOURCE_SHEET = "global"
ALPHABET_DEST_SHEET = "alphabet"
GOOGLE_DEST_SHEET = "google"
CLOUD_DEST_SHEET = "cloud"
PRIVATE_DEST_SHEET = "private"  # Note: The prompt included a space. Google Sheets usually trims this.


# If your sheet is actually named "cloud ", change this to "'cloud '"
# to ensure the API call works correctly.

def get_credentials():
    """
    Handles user authentication for Google APIs.
    Loads credentials from token.json if it exists, otherwise,
    initiates an OAuth2 flow using credentials.json.
    """
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # You must have a 'credentials.json' file from Google Cloud Console.
            if not os.path.exists("credentials.json"):
                print("Error: credentials.json not found. Please follow the setup instructions.")
                return None
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def extract_file_id_from_url(url):
    """Extracts the Google Drive file ID from a URL using regex."""
    match = re.search(r"/d/([a-zA-Z0-9-_]+)", url)
    if match:
        return match.group(1)
    return None


def clear_sheet(sheet_api, sheet_name):
    """Safely clears a sheet, handling cases where the sheet might not exist."""
    try:
        sheet_api.values().clear(spreadsheetId=SPREADSHEET_ID, range=sheet_name).execute()
        print(f"Sheet '{sheet_name}' cleared.")
    except HttpError as e:
        # If the error is because the sheet doesn't exist, print a warning and continue.
        if "Unable to parse range" in str(e):
            print(f"Warning: Sheet '{sheet_name}' not found. Please create it. Skipping clearing.")
        else:
            # For other errors, re-raise the exception.
            raise e


def main():
    """
    Main function to orchestrate reading from the sheet, analyzing
    permissions, and writing the results back.
    """
    print("Starting permission analysis...")
    creds = get_credentials()
    if not creds:
        return

    try:
        # Build the API clients for Sheets and Drive
        sheets_service = build("sheets", "v4", credentials=creds)
        drive_service = build("drive", "v3", credentials=creds)

        # 1. Read all URLs from column D of the 'global' sheet
        sheet_api = sheets_service.spreadsheets()

        # Clear the destination sheets before writing new data
        print("Clearing destination sheets...")
        clear_sheet(sheet_api, ALPHABET_DEST_SHEET)
        clear_sheet(sheet_api, GOOGLE_DEST_SHEET)
        clear_sheet(sheet_api, CLOUD_DEST_SHEET)
        clear_sheet(sheet_api, PRIVATE_DEST_SHEET)

        result = (
            sheet_api.values()
            .get(spreadsheetId=SPREADSHEET_ID, range=f"{SOURCE_SHEET}!D2:D")
            .execute()
        )
        url_rows = result.get("values", [])

        if not url_rows:
            print(f"No URLs found in column D of the '{SOURCE_SHEET}' sheet.")
            return

        alphabet_files = []
        google_files = []
        cloud_files = []
        private_files = []

        print(f"Found {len(url_rows)} URLs to analyze...")

        # 2. Analyze permissions for each URL
        for i, row in enumerate(url_rows):
            if not row:
                continue
            url = row[0]
            file_id = extract_file_id_from_url(url)
            if not file_id:
                print(f"Warning: Could not extract file ID from URL: {url}")
                continue

            print(f"  ({i + 1}/{len(url_rows)}) Analyzing file: {file_id}...")

            try:
                # Get file name and permissions with a single API call
                file_metadata = drive_service.files().get(
                    fileId=file_id, fields="name, permissions(type, role, domain)"
                ).execute()

                file_name = file_metadata.get("name")
                permissions = file_metadata.get("permissions", [])

                print(f"    -> Analyzing permissions for '{file_name}'...")
                if not permissions:
                    print("    -> No explicit permissions found. File is likely private to the owner.")
                    private_files.append([file_name])

                for p in permissions:
                    # ADDED: Detailed logging to help debug mismatched domains.
                    # Check your console output for this line to see the actual domains.
                    print(
                        f"      - Found permission: Type='{p.get('type')}', Role='{p.get('role')}', Domain='{p.get('domain')}'")

                    # We are looking for files shared with a whole domain as 'viewers' (reader role)
                    if p.get("role") == "reader" and p.get("type") == "domain":
                        domain = p.get("domain")
                        # IMPORTANT: You may need to change these domain values based on the console output above.
                        if domain == "alphabet.com":  # This is a hypothetical domain
                            alphabet_files.append([file_name])
                            print(f"    -> MATCH: '{file_name}' matches 'alphabet' criteria.")
                        elif domain == "google.com":
                            google_files.append([file_name])
                            print(f"    -> MATCH: '{file_name}' matches 'google' criteria.")
                        elif domain == "cloud.google.com":  # Also hypothetical
                            cloud_files.append([file_name])
                            print(f"    -> MATCH: '{file_name}' matches 'cloud' criteria.")

            except HttpError as error:
                print(f"    -> Error analyzing file ID {file_id}: {error.reason}")
                continue

        # 3. Write the categorized file names back to the spreadsheet
        print("\nWriting results to spreadsheet...")

        if not alphabet_files and not google_files and not cloud_files and not private_files:
            print("No files matched the specified criteria. Nothing to write.")

        if alphabet_files:
            body = {"values": alphabet_files}
            sheet_api.values().append(
                spreadsheetId=SPREADSHEET_ID,
                range=ALPHABET_DEST_SHEET,
                valueInputOption="RAW",
                body=body,
            ).execute()
            print(f"Wrote {len(alphabet_files)} file names to the '{ALPHABET_DEST_SHEET}' sheet.")

        if google_files:
            body = {"values": google_files}
            sheet_api.values().append(
                spreadsheetId=SPREADSHEET_ID,
                range=GOOGLE_DEST_SHEET,
                valueInputOption="RAW",
                body=body,
            ).execute()
            print(f"Wrote {len(google_files)} file names to the '{GOOGLE_DEST_SHEET}' sheet.")

        if cloud_files:
            body = {"values": cloud_files}
            sheet_api.values().append(
                spreadsheetId=SPREADSHEET_ID,
                range=CLOUD_DEST_SHEET,
                valueInputOption="RAW",
                body=body,
            ).execute()
            print(f"Wrote {len(cloud_files)} file names to the '{CLOUD_DEST_SHEET}' sheet.")

        if private_files:
            body = {"values": private_files}
            sheet_api.values().append(
                spreadsheetId=SPREADSHEET_ID,
                range=PRIVATE_DEST_SHEET,
                valueInputOption="RAW",
                body=body,
            ).execute()
            print(f"Wrote {len(private_files)} file names to the '{PRIVATE_DEST_SHEET}' sheet.")

        print("\nScript finished successfully.")

    except HttpError as err:
        print(f"\nA critical API error occurred: {err}")


if __name__ == "__main__":
    main()



