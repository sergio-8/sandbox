# main.py
#
# Python script to create shortcuts in a Google Drive folder
# based on a list of document links from a Google Sheet,
# using OAuth 2.0 for personal account authentication.

# --- Standard Library Imports ---
import re  # For regular expression matching to extract file IDs
import os.path  # For checking if token.json exists

# --- Third-party Library Imports ---
# Make sure to install these libraries:
# pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError



# --- Configuration ---
# IMPORTANT: Please fill in these details before running the script.

# Path to your OAuth 2.0 client secrets JSON file (downloaded from Google Cloud Console).
# Rename the downloaded file to 'credentials.json' or update this path.
PATH_TO_OAUTH_CREDS_JSON = 'credentials.json'
#
# Python script to create shortcuts in a Google Drive folder
# based on a list of document links from a Google Sheet,
# using OAuth 2.0 for personal account authentication.

# --- Standard Library Imports ---
import re # For regular expression matching to extract file IDs
import os.path # For checking if token.json exists

# --- Third-party Library Imports ---
# Make sure to install these libraries:
# pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# --- Configuration ---
# IMPORTANT: Please fill in these details before running the script.

# Path to your OAuth 2.0 client secrets JSON file (downloaded from Google Cloud Console).
# Rename the downloaded file to 'credentials.json' or update this path.
PATH_TO_OAUTH_CREDS_JSON = 'credentials.json'

# The ID of the Google Sheet containing the document links.
# You can find this in the URL of your Google Sheet (e.g., https://docs.google.com/spreadsheets/d/SHEET_ID/edit)
GOOGLE_SHEET_ID = '11nRneTt1VoZhU7Svj2iPH9rTbvT9yEqrIdmvgw5Ztic'

# The range in your Google Sheet that contains the links.
# Example: 'Sheet1!A2:A' (for all links in column A starting from row 2 of Sheet1)
# Example: 'My Links!B1:B50' (for links in column B, rows 1-50 of sheet named 'My Links')
SHEET_RANGE_WITH_LINKS = 'Sheet1!A1:A' # Adjust as needed

# The ID of the Google Drive folder where you want to create the shortcuts.
# You can find this in the URL when you have the folder open in Google Drive
# (e.g., https://drive.google.com/drive/folders/FOLDER_ID)
TARGET_DRIVE_FOLDER_ID = '1NIhqt2KrXfTkB2KjrgafzhgsBSk5KryM'

# Scopes required by the script.
# - Read-only access to Google Sheets.
# - Full access to Google Drive to create shortcuts and read file metadata (for names).
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/drive' # Full Drive scope to create shortcuts and get names
]

# File to store the user's access and refresh tokens.
# This will be created automatically after the first successful authorization.
TOKEN_JSON_PATH = 'token.json'


# --- Helper Functions ---

def extract_file_id_from_url(url: str) -> str | None:
    """
    Extracts the Google Drive file ID from various common Google Drive URL formats.

    Args:
        url: The Google Drive URL string.

    Returns:
        The extracted file ID, or None if no ID could be found.
    """
    if not url or not isinstance(url, str):
        return None

    patterns = [
        r"/file/d/([a-zA-Z0-9_-]+)",
        r"/document/d/([a-zA-Z0-9_-]+)",
        r"/spreadsheets/d/([a-zA-Z0-9_-]+)",
        r"/presentation/d/([a-zA-Z0-9_-]+)",
        r"/drawings/d/([a-zA-Z0-9_-]+)",
        r"id=([a-zA-Z0-9_-]+)",
        r"/folders/([a-zA-Z0-9_-]+)"
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    if len(url) > 30 and not url.startswith("http") and " " not in url:
        if re.match(r"^[a-zA-Z0-9_-]+$", url):
            return url

    return None


def get_original_filename(drive_service, file_id: str) -> str:
    """
    Retrieves the original filename of a Google Drive file.

    Args:
        drive_service: The authenticated Google Drive API service instance.
        file_id: The ID of the file whose name is to be fetched.

    Returns:
        The name of the file, or a fallback name if an error occurs or name is not found.
    """
    try:
        file_metadata = drive_service.files().get(fileId=file_id, fields='name', supportsAllDrives=True).execute()
        return file_metadata.get('name', f"Untitled Shortcut to {file_id}")
    except HttpError as error:
        print(f"  Error fetching filename for {file_id}: {error.resp.status} {error.resp.reason}")
        # print(f"  Error details: {error.content.decode()}") # Can be verbose
        return f"Shortcut to {file_id} (name unavailable)"
    except Exception as e:
        print(f"  A non-HTTP error occurred while fetching filename for {file_id}: {e}")
        return f"Shortcut to {file_id} (name unavailable)"


def get_existing_shortcut_target_ids(drive_service, folder_id: str) -> set:
    """
    Retrieves a set of target IDs for all existing shortcuts in the specified folder.

    Args:
        drive_service: The authenticated Google Drive API service instance.
        folder_id: The ID of the folder to scan for shortcuts.

    Returns:
        A set of strings, where each string is a targetId of an existing shortcut.
    """
    existing_target_ids = set()
    page_token = None
    print(f"  Scanning folder '{folder_id}' for existing shortcuts...")
    try:
        while True:
            response = drive_service.files().list(
                q=f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.shortcut' and trashed=false",
                fields="nextPageToken, files(id, name, shortcutDetails)",
                pageToken=page_token,
                supportsAllDrives=True,
                includeItemsFromAllDrives=True  # Ensure visibility for shared drives
            ).execute()

            for file_item in response.get('files', []):
                shortcut_details = file_item.get('shortcutDetails')
                if shortcut_details and shortcut_details.get('targetId'):
                    existing_target_ids.add(shortcut_details['targetId'])

            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        print(f"  Found {len(existing_target_ids)} existing shortcut target(s) in the folder.")
    except HttpError as error:
        print(
            f"  ERROR: Could not list existing shortcuts in folder '{folder_id}': {error.resp.status} {error.resp.reason}")
        # print(f"  Details: {error.content.decode()}") # Can be verbose
        # If we can't list, we can't deduplicate, but maybe allow creation?
        # For now, assume an error here is critical for deduplication.
    return existing_target_ids


# --- Main Script Logic ---

def authenticate_user():
    """
    Authenticates the user using OAuth 2.0 flow.
    Loads existing credentials from token.json if available,
    otherwise runs the flow and saves new credentials.

    Returns:
        google.oauth2.credentials.Credentials: The authenticated credentials.
    """
    creds = None
    if os.path.exists(TOKEN_JSON_PATH):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_JSON_PATH, SCOPES)
            # print(f"Loaded credentials from '{TOKEN_JSON_PATH}'.") # Less verbose
        except Exception as e:
            print(f"Error loading credentials from '{TOKEN_JSON_PATH}': {e}. Will attempt re-authentication.")
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                print("Credentials expired. Attempting to refresh token...")
                creds.refresh(Request())
                print("Token refreshed successfully.")
            except Exception as e:
                print(f"Failed to refresh token: {e}. Need to re-authorize.")
                creds = None
        else:
            print(f"No valid credentials found or refresh failed. Starting new authentication flow...")
            if not os.path.exists(PATH_TO_OAUTH_CREDS_JSON):
                print(f"ERROR: OAuth credentials file ('{PATH_TO_OAUTH_CREDS_JSON}') not found.")
                return None
            try:
                flow = InstalledAppFlow.from_client_secrets_file(PATH_TO_OAUTH_CREDS_JSON, SCOPES)
                creds = flow.run_local_server(port=0)
                print("Authentication successful.")
            except FileNotFoundError:
                print(f"ERROR: OAuth credentials file ('{PATH_TO_OAUTH_CREDS_JSON}') not found during flow.")
                return None
            except Exception as e:
                print(f"An error occurred during the authentication flow: {e}")
                return None
        if creds:
            try:
                with open(TOKEN_JSON_PATH, 'w') as token_file:
                    token_file.write(creds.to_json())
                print(f"Credentials saved to '{TOKEN_JSON_PATH}'.")
            except Exception as e:
                print(f"Error saving token to '{TOKEN_JSON_PATH}': {e}")
    return creds


def main():
    """
    Main function to execute the script.
    Authenticates, reads links from Google Sheets, and creates shortcuts in Google Drive.
    """
    print("Starting Google Drive Shortcut Creator Script (OAuth Flow with Deduplication)...")

    # --- Validate Configuration ---
    if 'YOUR_GOOGLE_SHEET_ID' in GOOGLE_SHEET_ID or \
            'YOUR_TARGET_GOOGLE_DRIVE_FOLDER_ID' in TARGET_DRIVE_FOLDER_ID:
        print("\nERROR: Please update the configuration variables at the top of the script.")
        return

    if not os.path.exists(PATH_TO_OAUTH_CREDS_JSON):
        print(f"\nERROR: OAuth credentials file '{PATH_TO_OAUTH_CREDS_JSON}' not found.")
        return

    # 1. Authenticate and Initialize Services
    print("\nStep 1: Authentication")
    creds = authenticate_user()
    if not creds:
        print("Authentication failed. Exiting script.")
        return
    print("Successfully authenticated.")

    drive_service = None
    sheets_service = None
    try:
        drive_service = build('drive', 'v3', credentials=creds)
        sheets_service = build('sheets', 'v4', credentials=creds)
        print("Successfully initialized Google Drive and Sheets API services.")
    except HttpError as error:
        print(f"ERROR: Failed to build Google API services: {error}")
        return
    except Exception as e:
        print(f"ERROR: An unexpected error occurred while building services: {e}")
        return

    # Pre-fetch existing shortcut target IDs from the target folder for deduplication
    print("\nPreparing for deduplication:")
    existing_shortcut_target_ids = get_existing_shortcut_target_ids(drive_service, TARGET_DRIVE_FOLDER_ID)

    # 2. Read Links from Google Sheet
    print("\nStep 2: Reading Links from Google Sheet")
    doc_links_with_sources = []
    try:
        range_to_get = SHEET_RANGE_WITH_LINKS
        if '!' not in range_to_get:
            print(
                f"  Warning: SHEET_RANGE_WITH_LINKS ('{SHEET_RANGE_WITH_LINKS}') does not specify a sheet name. Assuming it applies to the first sheet.")

        result = sheets_service.spreadsheets().values().get(
            spreadsheetId=GOOGLE_SHEET_ID,
            range=range_to_get
        ).execute()
        values = result.get('values', [])

        if not values:
            print(f"  No data found in Google Sheet '{GOOGLE_SHEET_ID}' at range '{SHEET_RANGE_WITH_LINKS}'.")
            return
        else:
            current_sheet_name = SHEET_RANGE_WITH_LINKS.split('!')[0] if '!' in SHEET_RANGE_WITH_LINKS else "FirstSheet"
            start_row_match = re.search(r'([A-Z]+)([0-9]+):', SHEET_RANGE_WITH_LINKS.split('!')[-1])
            start_row_offset = int(start_row_match.group(2)) if start_row_match else 1

            for i, row_data in enumerate(values):
                if row_data and len(row_data) > 0 and row_data[0] and str(row_data[0]).strip():
                    link_url = str(row_data[0]).strip()
                    cell_ref = f"{current_sheet_name}!{SHEET_RANGE_WITH_LINKS.split('!')[-1].split(':')[0][0]}{start_row_offset + i}"
                    doc_links_with_sources.append((link_url, cell_ref))
                elif row_data and (len(row_data) == 0 or not row_data[0] or not str(row_data[0]).strip()):
                    cell_ref = f"{current_sheet_name}!{SHEET_RANGE_WITH_LINKS.split('!')[-1].split(':')[0][0]}{start_row_offset + i}"
                    print(f"  Skipping empty or invalid link in cell {cell_ref}.")

            print(f"  Found {len(doc_links_with_sources)} potential link(s) in the Google Sheet.")
            if not doc_links_with_sources:
                print("  No valid links found to process.")
                return

    except HttpError as error:
        print(f"ERROR: An error occurred while reading from Google Sheet: {error.resp.status} {error.resp.reason}")
        print(f"Details: {error.content.decode()}")
        return
    except Exception as e:
        print(f"ERROR: An unexpected error occurred while reading sheet: {e}")
        return

    # 3. Create Shortcuts in Google Drive
    print(f"\nStep 3: Processing and Creating Shortcuts in Target Folder (ID: {TARGET_DRIVE_FOLDER_ID})")
    if not doc_links_with_sources:
        print("  No document links were successfully read from the sheet. Nothing to process.")
        return

    success_count = 0
    failure_count = 0
    skipped_count = 0

    for link_url, source_cell in doc_links_with_sources:
        print(f"\nProcessing URL from {source_cell}: {link_url}")

        target_file_id = extract_file_id_from_url(link_url)

        if not target_file_id:
            print(f"  Could not extract a valid Google Drive file ID from URL: '{link_url}'. Skipping.")
            failure_count += 1
            continue

        print(f"  Extracted Target File ID: {target_file_id}")

        # --- Deduplication Check ---
        if target_file_id in existing_shortcut_target_ids:
            print(f"  SKIPPED: A shortcut to target ID '{target_file_id}' already exists in the target folder.")
            skipped_count += 1
            continue
        # --- End Deduplication Check ---

        shortcut_name = get_original_filename(drive_service, target_file_id)

        if "(name unavailable)" in shortcut_name and "Shortcut to" in shortcut_name:
            print(
                f"  Warning: Could not retrieve original name for target ID {target_file_id}. Your account might not have access to this file.")

        print(f"  Using shortcut name: '{shortcut_name}'")

        shortcut_metadata = {
            'name': shortcut_name,
            'mimeType': 'application/vnd.google-apps.shortcut',
            'shortcutDetails': {
                'targetId': target_file_id
            },
            'parents': [TARGET_DRIVE_FOLDER_ID]
        }

        try:
            shortcut = drive_service.files().create(
                body=shortcut_metadata,
                fields='id,name,shortcutDetails,webViewLink',
                supportsAllDrives=True
            ).execute()
            print(f"  SUCCESS: Created shortcut '{shortcut.get('name')}' (ID: {shortcut.get('id')})")
            print(f"           -> Pointing to target ID: {shortcut.get('shortcutDetails', {}).get('targetId')}")
            print(f"           Shortcut Link: {shortcut.get('webViewLink')}")
            # Add the newly created shortcut's target ID to our set to prevent
            # duplicates if the same link appears multiple times IN THE CURRENT SHEET RUN.
            existing_shortcut_target_ids.add(target_file_id)
            success_count += 1
        except HttpError as error:
            error_status = error.resp.status
            error_reason = error.resp.reason
            error_details = error.content.decode()
            print(
                f"  ERROR creating shortcut for target ID {target_file_id} (from URL {link_url}): {error_status} {error_reason}")
            # print(f"  Details: {error_details}") # Can be verbose
            failure_count += 1
        except Exception as e:
            print(f"  An unexpected non-HTTP error occurred while creating shortcut for {link_url}: {e}")
            failure_count += 1

    print("\n--- Script Finished ---")
    print(f"Total links processed from sheet: {len(doc_links_with_sources)}")
    print(f"Successfully created shortcuts: {success_count}")
    print(f"Skipped (duplicates): {skipped_count}")
    print(f"Failed to process/create: {failure_count}")
    print("-------------------------\n")


if __name__ == '__main__':
    main()
