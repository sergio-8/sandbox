import os.path
import re
# pandas is not strictly needed if directly using Sheets API for links
# import pandas as pd

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these SCOPES, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly',  # Read from Sheets
    'https://www.googleapis.com/auth/drive'
    # Full Drive access (to read metadata, create shortcuts/folders, potentially move owned files)
]

# --- Configuration ---
SPREADSHEET_ID = '11nRneTt1VoZhU7Svj2iPH9rTbvT9yEqrIdmvgw5Ztic'
RANGE_NAME = 'Sheet1!A2:A'
TARGET_DRIVE_FOLDER_NAME = 'C****_OFFICIAL_DOCS_MAY_23'


def authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def get_google_doc_links(creds, spreadsheet_id, range_name):
    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        values = result.get('values', [])
        links = [row[0] for row in values if row]
        if not links:
            print('No data found in spreadsheet.')
        return links
    except HttpError as err:
        print(f"An API error occurred (Sheets): {err}")
        return []


def extract_file_id_from_url(url):
    match = re.search(r'/d/([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    match = re.search(r'id=([a-zA-Z0-9_-]+)', url)  # For older /open?id= links
    if match:
        return match.group(1)
    print(f"Could not extract file ID from URL: {url}")
    return None


def get_or_create_drive_folder(creds, folder_name):
    try:
        service = build('drive', 'v3', credentials=creds)
        query = f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}' and trashed=false"
        # Search in 'My Drive' primarily.
        # Adding 'and "root" in parents' could make it stricter for user's root if needed,
        # but Drive API search can be nuanced. For simplicity, we find by name.
        response = service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name)',
            supportsAllDrives=True,  # Good practice, though target is 'My Drive'
            includeItemsFromAllDrives=True  # Good practice
        ).execute()
        folders = response.get('files', [])

        # If multiple folders with the same name exist, this picks the first one.
        # You might want more specific logic if that's an issue (e.g., specify a parent for the target folder).
        if folders:
            folder_id = folders[0].get('id')
            print(f"Target folder '{folder_name}' found with ID: {folder_id}")
            return folder_id
        else:
            print(f"Target folder '{folder_name}' not found, creating it in your 'My Drive'...")
            file_metadata = {'name': folder_name, 'mimeType': 'application/vnd.google-apps.folder'}
            folder = service.files().create(body=file_metadata, fields='id', supportsAllDrives=True).execute()
            folder_id = folder.get('id')
            print(f"Target folder '{folder_name}' created with ID: {folder_id}")
            return folder_id
    except HttpError as error:
        print(f'An API error occurred (Drive - get/create folder): {error}')
        return None


def process_file_link(creds, original_file_id, target_folder_id):
    """
    Attempts to create a shortcut for the given file ID in the target folder.
    If the file is owned by the user, it could alternatively be moved (more complex logic).
    For simplicity and robustness with shared files, creating a shortcut is the primary goal.
    """
    try:
        drive_service = build('drive', 'v3', credentials=creds)

        # Get metadata of the original file to get its name for the shortcut
        original_file_metadata = drive_service.files().get(
            fileId=original_file_id,
            fields='name, id, ownedByMe, capabilities(canMoveItemOutOfDrive, canEdit)',  # Add more fields if needed
            supportsAllDrives=True
        ).execute()
        original_file_name = original_file_metadata.get('name', f"Shortcut to {original_file_id}")
        owned_by_me = original_file_metadata.get('ownedByMe', False)

        print(f"Processing file: '{original_file_name}' (ID: {original_file_id}), Owned by me: {owned_by_me}")

        # --- Primary Action: Create a Shortcut ---
        shortcut_metadata = {
            'name': original_file_name,  # Name of the shortcut file itself
            'mimeType': 'application/vnd.google-apps.shortcut',
            'shortcutDetails': {
                'targetId': original_file_id  # The ID of the file the shortcut points to
            },
            'parents': [target_folder_id]  # Place the shortcut in this folder
        }

        try:
            # Check if a shortcut with the same name and target already exists in the folder
            # This query can be complex and slow if there are many files.
            # A simpler approach is to just try creating it and handle potential duplicate errors if Google Drive API provides them,
            # or allow multiple shortcuts if desired. For now, we'll just create.

            existing_shortcuts_query = f"mimeType='application/vnd.google-apps.shortcut' and name='{original_file_name.replace("'" , " \\'")}' and '{target_folder_id}' in parents and shortcutDetails.targetId='{original_file_id}' and trashed=false"
            response = drive_service.files().list(
                q=existing_shortcuts_query,
                fields='files(id)',
                supportsAllDrives=True,
                includeItemsFromAllDrives=True
            ).execute()

            if response.get('files'):
                print(f"Shortcut for '{original_file_name}' already exists in the target folder. Skipping creation.")
            return True

            drive_service.files().create(body=shortcut_metadata, supportsAllDrives=True).execute()
            print(f"Successfully created shortcut for '{original_file_name}' in folder ID {target_folder_id}")
            return True
        except HttpError as error_shortcut:
            print(
                f"Failed to create shortcut for '{original_file_name}' (ID: {original_file_id}). Error: {error_shortcut}")
            # As a fallback for owned files, one *could* attempt a move, but this makes the script's intent less clear.
            # Sticking to shortcuts for shared items is generally safer.
            # if owned_by_me:
            #    print(f"Shortcut creation failed. Since you own '{original_file_name}', you could implement a 'move' logic here.")
            return False

    except HttpError as error:
        print(f"An API error occurred processing file ID {original_file_id}: {error}")
        return False
    except Exception as e:  # Catch any other unexpected errors
        print(f"An unexpected error occurred processing file ID {original_file_id}: {e}")
        return False


def main():
    creds = authenticate()
    if not creds:
        print("Failed to authenticate.")
        return

    print(f"Fetching links from Spreadsheet ID: {SPREADSHEET_ID}, Range: {RANGE_NAME}")
    doc_links = get_google_doc_links(creds, SPREADSHEET_ID, RANGE_NAME)

    if not doc_links:
        return

    target_folder_id = get_or_create_drive_folder(creds, TARGET_DRIVE_FOLDER_NAME)
    if not target_folder_id:
        print("Could not find or create the target Drive folder. Exiting.")
        return

    print(
        f"\nAttempting to process {len(doc_links)} documents into folder '{TARGET_DRIVE_FOLDER_NAME}' ({target_folder_id})...")
    success_count = 0
    failure_count = 0

    for link_idx, link in enumerate(doc_links):
        print(f"\n--- Processing link {link_idx + 1}/{len(doc_links)}: {link} ---")
        file_id = extract_file_id_from_url(link)
        if file_id:
            if process_file_link(creds, file_id, target_folder_id):
                success_count += 1
            else:
                failure_count += 1
        else:
            print(f"Skipping invalid link or link without a parsable file ID: {link}")
            failure_count += 1  # Count as failure if ID cannot be extracted

    print(f"\n--- Process Complete ---")
    print(f"Successfully processed (e.g., created shortcuts for): {success_count} documents.")
    print(f"Failed to process: {failure_count} documents.")


if __name__ == '__main__':
    # SPREADSHEET_ID = input("Enter your Google Spreadsheet ID: ")
    # RANGE_NAME = input("Enter the sheet name and range (e.g., Sheet1!A2:A): ")
    # TARGET_DRIVE_FOLDER_NAME = input("Enter name for Google Drive folder: ")
    main()