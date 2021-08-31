from pathlib import Path
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def connect_to_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    return drive


def createRemoteFolder(drive, folderName, parentID=0):

    folderlist = drive.ListFile(
        {"q": "mimeType='application/vnd.google-apps.folder' and trashed=false"}
    ).GetList()

    titlelist = [x["title"] for x in folderlist]
    if folderName in titlelist:
        for item in folderlist:
            if item["title"] == folderName:
                return item["id"]

    if parentID != 0:
        file_metadata = {
            "title": folderName,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [{"id": parentID}],
        }
    else:
        file_metadata = {
            "title": folderName,
            "mimeType": "application/vnd.google-apps.folder",
        }
    file0 = drive.CreateFile(file_metadata)
    file0.Upload()
    return file0["id"]


# Configuration
party_rank_name = "Nonoc"
player_list = ["EruisKawaii", "Husa", "xSardine", "etc"]
# Configuration


file_name = party_rank_name + " Anime Songs Ranking Sheet.xlsx"


def upload_every_xlsx():

    print("Connecting to Google Drive API...")
    drive = connect_to_drive()
    print("Connection successful!")

    print("Uploading files...")
    dir1 = createRemoteFolder(drive, "Party Ranks")
    dir2 = createRemoteFolder(drive, party_rank_name, dir1)

    # Search for any .xlsx file in the current directory or subdirectory
    sheet_path = Path(".")
    sheet_list = list(sheet_path.glob("**/*.xlsx"))
    for sheet in sheet_list:
        if str(sheet).startswith(party_rank_name):
            for player in player_list:
                file1 = drive.CreateFile(
                    {
                        "title": str(Path(file_name).with_suffix(""))
                        + " ("
                        + player
                        + ").xlsx",
                        "parents": [{"kind": "drive#fileLink", "id": dir2}],
                    }
                )  # Create GoogleDriveFile instance
                file1.SetContentFile(
                    sheet_list[0]
                )  # Set content of the file from given file.
                file1.Upload()
    print("Done :)")


if __name__ == "__main__":

    upload_every_xlsx()
