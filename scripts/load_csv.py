import pandas as pd
import requests
import math
import numpy as np
import os

#API_URL = "http://127.0.0.1:8000/api/v1"                                   #local
API_URL = "https://globant-api-340695378961.us-central1.run.app/api/v1"     #cloud run

def upload_csv_in_batches(file_path, endpoint, columns):
    if not os.path.exists(file_path):
        print(f"Error: file {file_path} not found.")
        return

    print(f"\nProcessing {file_path}...")
    df = pd.read_csv(file_path, header=None, names=columns)
    df = df.replace({np.nan: None})

    batch_size = 1000
    total_batches = math.ceil(len(df) / batch_size)

    for i in range(total_batches):
        start_idx = i * batch_size
        end_idx = start_idx + batch_size
        batch_df = df.iloc[start_idx:end_idx]
        records = batch_df.to_dict(orient="records")
        payload = {"items": records}
        response = requests.post(f"{API_URL}/{endpoint}", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print(f"Batch {i+1}/{total_batches} -> Inserted: {result['inserted']} | Failures: {result['failed']}")
        else:
            print(f"Error en Lote {i+1}: {response.text}")

if __name__ == "__main__":
    upload_csv_in_batches("data/departments.csv", "departments/batch", ["id", "department"])
    upload_csv_in_batches("data/jobs.csv", "jobs/batch", ["id", "job"])
    upload_csv_in_batches("data/hired_employees.csv", "employees/batch", ["id", "name", "datetime", "department_id", "job_id"])