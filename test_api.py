import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_hello():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Hello world"

def test_predict():
    response = client.post("/predict", json=[{
        "TV": 100.0,
        "Radio": 20.0,
        "Newspaper": 10.0
    }])
    assert response.status_code == 200
    assert "predictions" in response.json()

def test_ingest():
    response = client.post("/ingest", json={
        "TV": 230.1,
        "Radio": 37.8,
        "Newspaper": 69.2,
        "Sales": 22.1
    })
    assert response.status_code == 200
    assert response.json() == {"message": "Data ingested successfully"}

def test_retrain():
    response = client.post("/retrain")
    assert response.status_code == 200
    assert response.json() == {"message": "Model retrained successfully"}