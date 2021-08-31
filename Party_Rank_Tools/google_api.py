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
