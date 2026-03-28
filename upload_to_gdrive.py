# upload_to_gdrive.py
import os
from upload.auth import get_credentials
from upload.drive import get_drive_service, create_folder, generate_folder_name
from upload.uploader import upload_model, upload_file


def main():
    root_folder_id = os.environ["GDRIVE_FOLDER_ID"]

    credentials = get_credentials()
    service = get_drive_service(credentials)

    # buat folder baru tiap run
    folder_name = generate_folder_name()
    run_folder_id = create_folder(service, folder_name, root_folder_id)
    print("Folder created:", folder_name)

    # buat folder model di dalam run folder
    model_folder_id = create_folder(service, "model", run_folder_id)
    print("Model folder created:", "model")
    eda_folder_id = create_folder(service, "eda", run_folder_id)
    print("Model folder created:", "eda")

    local_model_folder = "preprocessing/model"
    local_eda_folder = "preprocessing/eda"

    # upload model folder
    upload_model(service, local_model_folder, model_folder_id)
    upload_model(service, local_eda_folder, model_folder_id)
    # upload csv
    model_csv_files = [
        "preprocessing/train_processed.csv",
        "preprocessing/test_processed.csv",
    ]
    eda_csv_files = [
        "preprocessing/eda/eda_summary.txt",
    ]

    for file in model_csv_files:
        upload_file(service, file, run_folder_id)
    for file in eda_csv_files:
        upload_file(service, file, eda_folder_id)


if __name__ == "__main__":
    main()
