import os.path
import io
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
import re  # For extracting the file ID from the URL

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']  # Read-only access is sufficient for export


def authenticate():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Ensure 'credentials.json' is in the same directory as the script
            if not os.path.exists('credentials.json'):
                print("Error: 'credentials.json' not found. Please download it from Google Cloud Console.")
                return None
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def extract_presentation_id(slides_url):
    """
    Extracts the presentation ID from a Google Slides URL.
    Example URL: https://docs.google.com/presentation/d/PRESENTATION_ID/edit
    """
    # Regex to find the ID in common Google Slides URL patterns
    match = re.search(r'/presentation/d/([^/]+)', slides_url)
    if match:
        return match.group(1)
    else:
        # Fallback for potentially different URL structures or if just ID is passed
        # This part might need adjustment if URLs are very different
        if 'docs.google.com' not in slides_url and len(slides_url) > 40:  # Heuristic for a raw ID
            return slides_url
        print("Error: Could not extract Presentation ID from the URL.")
        print(
            "Please ensure the URL is a valid Google Slides URL, e.g., https://docs.google.com/presentation/d/YOUR_ID/edit")
        return None


def export_slide_to_pdf(slides_url, output_pdf_filename="presentation.pdf"):
    """
    Authenticates, then exports a Google Slide presentation to PDF.
    Args:
        slides_url (str): The full URL of the Google Slides presentation.
        output_pdf_filename (str): The name for the output PDF file.
    """
    creds = authenticate()
    if not creds:
        print("Authentication failed. Exiting.")
        return

    try:
        service = build('drive', 'v3', credentials=creds)

        presentation_id = extract_presentation_id(slides_url)
        if not presentation_id:
            return

        print(f"Attempting to export presentation with ID: {presentation_id}")

        request = service.files().export_media(fileId=presentation_id,
                                               mimeType='application/pdf')

        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(F'Download {int(status.progress() * 100)}%.')

        # Save the PDF content to a file
        fh.seek(0)  # Go to the beginning of the BytesIO buffer
        with open(output_pdf_filename, 'wb') as f:
            f.write(fh.read())
        print(f"Presentation successfully exported as '{output_pdf_filename}'")

    except HttpError as error:
        print(f'An API error occurred: {error}')
        print(f'Details: {error.resp.status}, {error._get_reason()}')
        if error.resp.status == 404:
            print("Error 404: File not found. Check the Presentation ID and your permissions.")
        elif error.resp.status == 403:
            print(
                "Error 403: Permission denied. Ensure the account has access to this slide and the Drive API is enabled.")
        fh = None  # Ensure fh is not used if an error occurs during download
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    # --- IMPORTANT ---
    # 1. First, manually go to your http://go/agentspace_onepager link in your browser.
    # 2. Copy the full URL from your browser's address bar once it loads the Google Slides.
    #    It will look something like: https://docs.google.com/presentation/d/xxxxxxx_YOUR_ID_xxxxxxx/edit
    # 3. Paste that full URL below:

    google_slides_url = "https://docs.google.com/presentation/d/1IEzcvdkg98XKLBMoLWFXAnLuazfelO4i5n0SfvM5kYU/edit?slide=id.g34415a9b632_0_165#slide=id.g34415a9b632_0_165"  # <--- PASTE YOUR FULL URL HERE

    if google_slides_url == "YOUR_GOOGLE_SLIDES_URL_HERE":
        print("Please update the 'google_slides_url' variable in the script with the actual Google Slides URL.")
    else:
        output_filename = "my_presentation.pdf"  # You can change the output PDF name here
        export_slide_to_pdf(google_slides_url, output_filename)