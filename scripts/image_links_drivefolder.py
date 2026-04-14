'''
Program takes as an argument a folder id for a Google Drive folder with images image1.png, image2.png ...
Executes a query to get the file id for each image
Combines file id with https://lh3.googleusercontent.com/d/ to form a URL https://lh3.googleusercontent.com/d/<file id> suitable for embedding in an html document
Writes the image name and URL to a file (links.txt)
'''
import os
import re
import sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


base_url = "https://lh3.googleusercontent.com/d/"
# Scope for reading file metadata
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def get_drive_service():
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
    return build('drive', 'v3', credentials=creds)

def list_files_in_folder(folder_id):
    service = get_drive_service()

    try:
        # Define the query to find files inside the specific folder
        # 'trashed = false' ensures we don't get deleted files
        query = f"'{folder_id}' in parents and trashed = false"
        
        # Execute the request
        results = service.files().list(
            q=query,
            fields="nextPageToken, files(id, name)"
        ).execute()
        
        items = results.get('files', []) # items is a list of dicts

        if not items:
            print('No files found in this folder.')
            return

        print(f"Found {len(items)} files. Writing to links.txt...")
        # Sort so that items appear in order image1.png, image2.png...
        items.sort(key=lambda x: int(re.findall(r'\d+', x['name'])[0])) 
        with open('links.txt', 'w') as f:
            for item in items:
                line = f"Name: {item['name']} | Link: {base_url}{item['id']}\n"
                f.write(line)

        print("Done! Check 'links.txt' for the results.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Argument to program should be your Folder ID
    # Found in the URL: drive.google.com/drive/folders/YOUR_FOLDER_ID
    if (len(sys.argv) > 1):
        TARGET_FOLDER_ID = sys.argv[1]
    else:
        print("Need to provide folder ID")
        sys.exit(1)
    list_files_in_folder(TARGET_FOLDER_ID)