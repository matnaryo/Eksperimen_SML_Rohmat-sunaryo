import os
from googleapiclient.http import MediaFileUpload
from .drive import get_or_create_folder


def upload_file(service, file_path, folder_id):
    from googleapiclient.http import MediaFileUpload
    import os

    file_name = os.path.basename(file_path)

    file_metadata = {"name": file_name, "parents": [folder_id]}

    media = MediaFileUpload(file_path, resumable=True)

    service.files().create(body=file_metadata, media_body=media, fields="id").execute()

    print(f"Uploaded file: {file_name}")


def upload_model(service, local_folder, root_folder_id):
    for root, dirs, files in os.walk(local_folder):
        # Tentukan path relatif
        relative_path = os.path.relpath(root, local_folder)

        # Buat folder di Drive sesuai struktur
        current_parent_id = root_folder_id

        if relative_path != ".":
            for part in relative_path.split(os.sep):
                current_parent_id = get_or_create_folder(
                    service, part, current_parent_id
                )

        # Upload semua file dalam folder ini
        for file in files:
            file_path = os.path.join(root, file)

            file_metadata = {
                "name": file,
                "parents": [current_parent_id],
            }

            media = MediaFileUpload(file_path, resumable=False)

            service.files().create(
                body=file_metadata,
                media_body=media,
                fields="id",
                supportsAllDrives=True,
            ).execute()

            print("Uploaded:", file_path)
