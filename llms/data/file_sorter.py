import os.path
import csv
from datetime import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.auth.exceptions import RefreshError
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Scopes allow reading Drive file metadata and editing Spreadsheets.
SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/spreadsheets",
]


def authenticate_google_apis():
    """Handles user authentication for the Google APIs."""
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


def write_data_to_sheet(creds, spreadsheet_id, sheet_name, data_to_write):
    """Creates a new sheet and writes the given data to it."""
    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()

        print(f"\nPreparing to write {len(data_to_write) - 1} records to sheet '{sheet_name}'...")

        # Add a new sheet, or clear it if it already exists.
        body = {
            'requests': [{'addSheet': {'properties': {'title': sheet_name}}}]
        }
        try:
            sheet.batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
            print(f"Created new sheet named '{sheet_name}'.")
        except HttpError as error:
            if "already exists" in str(error):
                print(f"Sheet '{sheet_name}' already exists. Clearing old data.")
                sheet.values().clear(
                    spreadsheetId=spreadsheet_id,
                    range=sheet_name
                ).execute()
            else:
                raise error

        # Write the data to the new sheet.
        update_body = {'values': data_to_write}
        sheet.values().update(
            spreadsheetId=spreadsheet_id,
            range=f"'{sheet_name}'!A1",
            valueInputOption="USER_ENTERED",
            body=update_body
        ).execute()

        print("Successfully wrote data to the spreadsheet.")
        print(f"You can view it here: https://docs.google.com/spreadsheets/d/{spreadsheet_id}")

    except HttpError as error:
        print(f"\nAn error occurred while writing to Google Sheets: {error}")
        print("Please ensure the Spreadsheet ID is correct and you have edit access.")


def main():
    """
    Main function to read CSV, find unique files, fetch metadata, sort,
    and write the result to a new sheet.
    """
    SPREADSHEET_ID = '1pYogcHk2eVy6AoUOJF2RLRozEoQ7vTUzutr68d_IbXU'
    CSV_FILENAME = "separate  - Sheet1.csv"

    if SPREADSHEET_ID == 'YOUR_SPREADSHEET_ID_HERE':
        print("Error: Please open the script and set the SPREADSHEET_ID variable.")
        return

    creds = authenticate_google_apis()
    if not creds:
        print("Could not authenticate. Exiting.")
        return

    try:
        drive_service = build("drive", "v3", credentials=creds)
        unique_files_metadata = {}  # Store metadata for unique files, keyed by file_id

        with open(CSV_FILENAME, mode='r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            print("Reading CSV and fetching metadata for unique files...")
            for row in reader:
                if not row: continue
                link = row[0].strip()
                file_id = get_file_id_from_url(link)

                # If we have a valid ID and haven't processed it yet...
                if file_id and file_id not in unique_files_metadata:
                    try:
                        # Fetch metadata ONLY for the new, unique file
                        file_metadata = drive_service.files().get(
                            fileId=file_id,
                            fields="name, modifiedTime",
                            supportsAllDrives=True
                        ).execute()

                        # Store the metadata in our dictionary
                        unique_files_metadata[file_id] = {
                            "name": file_metadata.get("name"),
                            "modifiedTime": file_metadata.get("modifiedTime"),
                            "link": link
                        }
                    except HttpError as error:
                        print(f"An error occurred for file ID {file_id}: {error}")

        if not unique_files_metadata:
            print("No valid files found or processed.")
            return

        # Convert the dictionary of unique files into a list
        list_of_unique_files = list(unique_files_metadata.values())

        # Sort the unique files by modifiedTime (newest first)
        sorted_unique_files = sorted(
            list_of_unique_files,
            key=lambda x: x['modifiedTime'],
            reverse=True
        )

        # Prepare the data for writing to the sheet
        headers = ["Last Modified", "Name", "Link"]
        data_to_write = [headers]
        for item in sorted_unique_files:
            modified_date = datetime.fromisoformat(item['modifiedTime'].replace('Z', '+00:00'))
            data_to_write.append([
                modified_date.strftime('%Y-%m-%d %H:%M:%S'),
                item['name'],
                item['link']
            ])

        # Call the function to write the sorted, unique data
        write_data_to_sheet(creds, SPREADSHEET_ID, "Unique Files - Sorted", data_to_write)

    except FileNotFoundError:
        print(f"Error: The file '{CSV_FILENAME}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()