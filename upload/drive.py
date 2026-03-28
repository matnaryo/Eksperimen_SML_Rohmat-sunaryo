from googleapiclient.discovery import build
from datetime import datetime


def get_drive_service(credentials):
    return build("drive", "v3", credentials=credentials)


def generate_folder_name():
    return datetime.now().strftime("run_%Y-%m-%d_%H-%M-%S")


def create_folder(service, name, parent_id):
    query = (
        f"name='{name}' and "
        f"'{parent_id}' in parents and "
        f"mimeType='application/vnd.google-apps.folder' and trashed=false"
    )

    results = (
        service.files()
        .list(
            q=query,
            fields="files(id)",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
        )
        .execute()
    )

    files = results.get("files", [])

    # Jika folder sudah ada
    if files:
        return files[0]["id"]

    # Jika belum ada → buat folder baru
    folder_metadata = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_id],
    }

    folder = (
        service.files()
        .create(
            body=folder_metadata,
            fields="id",
            supportsAllDrives=True,
        )
        .execute()
    )

    return folder["id"]
