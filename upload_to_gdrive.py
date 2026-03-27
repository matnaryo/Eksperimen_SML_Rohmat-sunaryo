import os
from upload.auth import get_credentials
from upload.drive import get_drive_service
from upload.uploader import upload_model


def main():
    root_folder_id = os.environ["GDRIVE_FOLDER_ID"]

    credentials = get_credentials()
    service = get_drive_service(credentials)

    upload_model(
        service,
        "preprocessing/model",
        root_folder_id,
    )


if __name__ == "__main__":
    main()
