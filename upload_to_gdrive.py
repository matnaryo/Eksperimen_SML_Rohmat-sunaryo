# upload_to_gdrive.py
import os
from upload.auth import get_credentials
from upload.drive import get_drive_service, create_folder, generate_folder_name
from upload.uploader import upload_model, upload_file


def main():
    # tentukan direktori di gdrive sesuai Drive ID
    root_dir = os.environ["GDRIVE_FOLDER_ID"]

    # ambil kredential OAuth2 untuk bisa login ke akun gdrive
    credentials = get_credentials()
    service = get_drive_service(credentials)

    # buat fdirektori utama app dengan nama unik
    app_dir_name = generate_folder_name()
    app_dir = create_folder(service, app_dir_name, root_dir)

    # buat direktori untuk model dan EDA di dalam direktori app utama
    model_dir = create_folder(service, "model", app_dir)
    eda_dir = create_folder(service, "eda", app_dir)

    # tentukan direktori local(runner) dari model dan EDA
    local_model_dir = "preprocessing/model"
    local_eda_dir = "preprocessing/eda"

    # upload direktori local ke gdrive sesuai kriteria
    upload_model(service, local_model_dir, model_dir)
    upload_model(service, local_eda_dir, eda_dir)

    # seleksi file csv dari local runner
    model_csv_files = [
        "preprocessing/train_processed.csv",
        "preprocessing/test_processed.csv",
    ]
    eda_csv_files = [
        "preprocessing/eda/eda_summary.txt",
    ]

    # upload file csv sesuai kriteria
    for file in model_csv_files:
        upload_file(service, file, app_dir)
    for csv in eda_csv_files:
        upload_file(service, csv, eda_dir)


if __name__ == "__main__":
    main()
