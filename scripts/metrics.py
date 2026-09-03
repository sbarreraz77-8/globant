import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000/api/v1/metrics"

def test_hires_by_quarter():
    print("")
    print("Number of employees hired for each job and department in 2021 divided by quarter")
    print("="*80)
    
    response = requests.get(f"{API_URL}/hires-by-quarter")
    
    if response.status_code == 200:
        data = response.json()
        if data:
            df = pd.DataFrame(data)
            print(df)
            print(f"\nTotal records: {len(df)}")
        else:
            print("No records")
    else:
        print(f"Error: {response.status_code} - {response.text}")

def test_departments_above_average():
    print("")
    print("Number of employees hired of each department that hired more employees than the mean of employees hired in 2021 ")
    print("="*80)
    
    response = requests.get(f"{API_URL}/departments-above-average")
    
    if response.status_code == 200:
        data = response.json()
        if data:
            df = pd.DataFrame(data)
            print(df)
            print(f"\nTotal records: {len(df)}")
        else:
            print("No records")
    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    try:
        test_hires_by_quarter()
        test_departments_above_average()
    except requests.exceptions.ConnectionError:
        print("\nError")