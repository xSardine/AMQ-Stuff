import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

party_rank_name = "Insert Party Rank Name.ods"
player_list = ["Player 1", "Player 2", "Player 3", "[...]", "Player X"]

SCOPES = [
    "https://www.googleapis.com/auth/docs",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.install",
]


def main():

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("drive", "v3", credentials=creds)

        # Create General Party Rank Folder
        file_metadata = {
            "name": f"{party_rank_name.split('.')[0]} PR",
            "mimeType": "application/vnd.google-apps.folder",
        }
        PRFolder = service.files().create(body=file_metadata, fields="id").execute()
        print(f"Created folder: {party_rank_name.split(' ')[0]} PR")

        for player in player_list:
            # Upload the sheet for the current user
            file_metadata = {
                "name": f"{party_rank_name.split(' ')[0]} ({player}).ods",
                "parents": [PRFolder.get("id")],
            }
            media = MediaFileUpload(
                "exampleSheet.ods",
                mimetype="application/vnd.oasis.opendocument.spreadsheet",
            )
            sheet = (
                service.files()
                .create(body=file_metadata, media_body=media, fields="id")
                .execute()
            )
            print(f"Created sheet: {party_rank_name.split(' ')[0]} ({player}).ods")
        print("Done :)")

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f"An error occurred: {error}")


if __name__ == "__main__":

    main()
