# 2. Import Library yang dibutuhkan
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import joblib
import sys
from io import StringIO

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "")

train_path = os.path.join(MODEL_DIR, "../loan_default.csv")
save_dir = os.path.join(MODEL_DIR, "model")


def auto_preprocess(train_path, save_dir=""):
    # Buat direktori penyimpanan model
    os.makedirs(save_dir, exist_ok=True)

    # 3. --- Load data ---
    data = pd.read_csv(train_path)

    # 4.--- EDA ---
    eda_file = os.path.join(save_dir, "../eda_summary.txt")
    with open(eda_file, "w") as f:
        f.write("=== Jumlah baris & kolom ===\n")
        f.write(f"{data.shape}\n\n")

        f.write("=== 5 baris teratas ===\n")
        f.write(f"{data.head().to_string()}\n\n")

        f.write("=== Info DataFrame ===\n")
        # info() tidak mengembalikan, jadi redirect ke string
        buffer = StringIO()
        data.info(buf=buffer)
        f.write(buffer.getvalue() + "\n")

        f.write("=== Statistik Deskriptif ===\n")
        f.write(f"{data.describe().to_string()}\n\n")

        f.write("=== Nilai unik kolom Default ===\n")
        f.write(f"{data['Default'].unique()}\n\n")

        f.write("=== Distribusi Default ===\n")
        f.write(f"{data['Default'].value_counts().to_string()}\n\n")

        f.write("=== Prosentase Default ===\n")
        f.write(f"{data['Default'].value_counts(normalize=True).to_string()}\n\n")

        f.write("=== Data Missing ===\n")
        f.write(f"{data.isnull().sum().to_string()}\n\n")

        f.write("=== Data Duplikat ===\n")
        f.write(f"{data.duplicated().sum()}\n\n")

    # Drop kolom LoanID
    data.drop("LoanID", axis=1, inplace=True)

    # 5. --- Split Data Latih dan Data Test ---
    data_train, data_test = train_test_split(
        data, test_size=0.05, random_state=42, shuffle=True
    )
    data_train.reset_index(drop=True, inplace=True)
    data_test.reset_index(drop=True, inplace=True)

    # 6. --- Pisahkan numerik & kategorikal ---
    numerical_columns = data_train.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()
    categorical_columns = data_train.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    # 7. --- Scaling numerik ---
    for col in numerical_columns:
        scaler = MinMaxScaler()
        # Fit & transform kolom pada train
        data_train[[col]] = scaler.fit_transform(data_train[[col]])
        # Transform kolom pada test jika ada
        if data_test is not None:
            data_test[[col]] = scaler.transform(data_test[[col]])
        # Simpan scaler per kolom
        joblib.dump(scaler, os.path.join(save_dir, f"scaler_{col}.joblib"))

    # 8. --- Encoding kategorikal ---
    for col in categorical_columns:
        encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
        encoder.fit(data_train[[col]])

        train_encoded = pd.DataFrame(
            encoder.transform(data_train[[col]]),
            columns=[f"{col}_{cat}" for cat in encoder.categories_[0]],
            index=data_train.index,
        )
        data_train = data_train.drop(columns=[col]).join(train_encoded)
        # Transform kolom pada test jika ada
        if data_test is not None:
            test_encoded = pd.DataFrame(
                encoder.transform(data_test[[col]]),
                columns=[f"{col}_{cat}" for cat in encoder.categories_[0]],
                index=data_test.index,
            )
            data_test = data_test.drop(columns=[col]).join(test_encoded)
        # Simpan scaler per kolom
        joblib.dump(encoder, f"{save_dir}/encoder_{col}.joblib")

    # 9. --- Simpan CSV hasil preprocessing ---
    train_csv = f"{save_dir}/../train_processed.csv"
    data_train.to_csv(train_csv, index=False)
    if data_test is not None:
        test_csv = f"{save_dir}/../test_processed.csv"
        data_test.to_csv(test_csv, index=False)
    else:
        test_csv = None

    print("Perintah sukses dijalankan")
    return data_train, data_test, train_csv, test_csv


auto_preprocess(train_path, save_dir)
