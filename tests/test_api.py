def test_ingest_departments_success(client):
    payload = {
        "items": [
            {"id": 1, "department": "Engineering"},
            {"id": 2, "department": "Human Resources"}
        ]
    }
    response = client.post("/api/v1/departments/batch", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["inserted"] == 2
    assert data["failed"] == 0

def test_ingest_batch_size_limit(client):
    payload = {
        "items": [{"id": i, "department": f"Dept {i}"} for i in range(1, 1002)]
    }
    response = client.post("/api/v1/departments/batch", json=payload)
    assert response.status_code == 422 

def test_ingest_employees_with_errors(client):
    
    client.post("/api/v1/departments/batch", json={"items": [{"id": 1, "department": "IT"}]})
    client.post("/api/v1/jobs/batch", json={"items": [{"id": 1, "job": "Data Engineer"}]})

    
    payload = {
        "items": [
            {"id": 1, "name": "Joan Barrera", "datetime": "2021-11-07T02:48:42Z", "department_id": 1, "job_id": 1},
            {"id": 2, "name": None, "datetime": "2021-11-07T02:48:42Z", "department_id": 1, "job_id": 1}
        ]
    }
    response = client.post("/api/v1/employees/batch", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["inserted"] == 1
    assert data["failed"] == 1