import os.path
import csv
from datetime import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.auth.exceptions import RefreshError
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# --- UPDATED SCOPES ---
# Added the 'spreadsheets' scope to allow writing to Google Sheets.
SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/spreadsheets",
]


def authenticate_google_drive():
    """Handles user authentication for Google APIs."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError:
                creds = None
        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def get_file_id_from_url(url):
    """Extracts the Google Drive file ID from its URL."""
    try:
        return url.split('/d/')[1].split('/')[0]
    except IndexError:
        print(f"Warning: Could not parse file ID from URL: {url}")
        return None


def write_to_spreadsheet(creds, spreadsheet_id, sorted_data):
    """Writes the sorted data to a new sheet in the specified spreadsheet."""
    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()

        new_sheet_name = "Sorted by Last Modified"

        # --- NEW: Prepare data for writing ---
        # Add a header row to the sorted data
        headers = ["Last Modified", "Name", "Link"]
        data_to_write = [headers]
        for item in sorted_data:
            modified_date = datetime.fromisoformat(item['modifiedTime'].replace('Z', '+00:00'))
            data_to_write.append([
                modified_date.strftime('%Y-%m-%d %H:%M:%S'),
                item['name'],
                item['link']
            ])

        # --- NEW: Add a new sheet (or clear it if it exists) ---
        body = {
            'requests': [{
                'addSheet': {
                    'properties': {
                        'title': new_sheet_name
                    }
                }
            }]
        }
        try:
            sheet.batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
            print(f"\nCreated new sheet named '{new_sheet_name}'.")
        except HttpError as error:
            if "already exists" in str(error):
                print(f"Sheet '{new_sheet_name}' already exists. Clearing old data.")
                sheet.values().clear(
                    spreadsheetId=spreadsheet_id,
                    range=new_sheet_name
                ).execute()
            else:
                raise error

        # --- NEW: Write the data to the new sheet ---
        update_body = {
            'values': data_to_write
        }
        sheet.values().update(
            spreadsheetId=spreadsheet_id,
            range=f"'{new_sheet_name}'!A1",
            valueInputOption="USER_ENTERED",
            body=update_body
        ).execute()

        print("Successfully wrote sorted list to the spreadsheet.")
        print(f"You can view it here: https://docs.google.com/spreadsheets/d/{spreadsheet_id}")

    except HttpError as error:
        print(f"\nAn error occurred while writing to Google Sheets: {error}")
        print("Please ensure the Spreadsheet ID is correct and you have edit access.")


def main():
    """
    Main function to read CSV, fetch file metadata, sort, and write results back to the spreadsheet.
    """
    SPREADSHEET_ID = '1pYogcHk2eVy6AoUOJF2RLRozEoQ7vTUzutr68d_IbXU'
    CSV_FILENAME = "separate  - Sheet1.csv"

    if SPREADSHEET_ID == 'YOUR_SPREADSHEET_ID_HERE':
        print("Error: Please open the script and set the SPREADSHEET_ID variable.")
        return

    creds = authenticate_google_drive()
    if not creds:
        print("Could not authenticate. Exiting.")
        return

    try:
        drive_service = build("drive", "v3", credentials=creds)
        files_with_metadata = []

        with open(CSV_FILENAME, mode='r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            print("Fetching metadata for each file...")
            for row in reader:
                if not row: continue
                link = row[0].strip()
                file_id = get_file_id_from_url(link)
                if file_id:
                    try:
                        # --- THIS IS THE LINE THAT WAS CHANGED ---
                        file_metadata = drive_service.files().get(
                            fileId=file_id,
                            fields="name, modifiedTime",
                            supportsAllDrives=True  # Add this parameter
                        ).execute()

                        files_with_metadata.append({
                            "name": file_metadata.get("name"),
                            "modifiedTime": file_metadata.get("modifiedTime"),
                            "link": link
                        })
                    except HttpError as error:
                        # This will now only print if there's a real issue
                        # like the file being deleted or a permission problem.
                        print(f"An error occurred for file ID {file_id}: {error}")

        if not files_with_metadata:
            print("No valid files found or processed.")
            print("Please ensure the account you logged in with has access to the documents.")
            return

        sorted_files = sorted(
            files_with_metadata, key=lambda x: x['modifiedTime'], reverse=True
        )

        write_to_spreadsheet(creds, SPREADSHEET_ID, sorted_files)

    except FileNotFoundError:
        print(f"Error: The file '{CSV_FILENAME}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()

