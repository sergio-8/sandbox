import re
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# CORRECTED SCOPE: Changed to a broader read-only scope
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# The URL of the Google Sheet you want to analyze.
FILE_URL = "https://docs.google.com/document/d/1MKZ6-EqkK3FT4BtrBtbEgmYhTubKh9AZRFqliJIYI5c/edit?pli=1&tab=t.jt3nil98lmj9#heading=h.3aeqpki4g6nq"


def get_file_id_from_url(url):
    """Extracts the Google Drive file ID from its URL using regex."""
    match = re.search(r'/d/([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    return None


def analyze_permissions():
    """
    Analyzes file permissions using Application Default Credentials (ADC).
    """
    try:
        creds, _ = google.auth.default(scopes=SCOPES)

        service = build('drive', 'v3', credentials=creds)

        file_id = get_file_id_from_url(FILE_URL)
        if not file_id:
            print("Could not extract File ID from the URL.")
            return

        file_metadata = service.files().get(
            fileId=file_id,
            fields='name, permissions'
        ).execute()

        file_name = file_metadata.get('name')
        permissions = file_metadata.get('permissions', [])

        print(f"📄 **Analysis for file:** '{file_name}'\n" + "-" * 35)

        if not permissions:
            print("No explicit sharing permissions found. Access may be restricted to the owner.")
            return

        for perm in permissions:
            role = perm['role'].capitalize()
            perm_type = perm['type']

            if perm_type == 'user':
                email = perm.get('emailAddress', 'N/A')
                print(f"👤 **User:** {email} ({role})")
            elif perm_type == 'group':
                email = perm.get('emailAddress', 'N/A')
                print(f"👥 **Group:** {email} ({role})")
            elif perm_type == 'domain':
                domain = perm.get('domain', 'N/A')
                print(f"🏢 **Domain:** Anyone at '{domain}' can {role.lower()}.")
            elif perm_type == 'anyone':
                print(f"🌍 **Public:** Anyone on the internet with the link can {role.lower()}.")

    except HttpError as error:
        print(f"An API error occurred: {error}")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("\nPlease ensure your environment is authenticated correctly.")
        print("You may need to run 'gcloud auth application-default login' again.")


if __name__ == '__main__':
    analyze_permissions()