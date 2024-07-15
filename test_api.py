from fastapi.testclient import TestClient
from main import app, Base, engine, SessionLocal, Advertising

client = TestClient(app)

def setup_module(module):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    db.query(Advertising).delete()
    db.commit()

def test_predict():
    response = client.post("/predict", json=[{"TV": 100.0, "Radio": 20.0, "Newspaper": 10.0}])
    assert response.status_code == 200
    assert "predictions" in response.json()

def test_ingest():
    response = client.post("/ingest", json={"TV": 100.0, "Radio": 20.0, "Newspaper": 10.0, "Sales": 15.0})
    assert response.status_code == 200
    assert response.json() == {"message": "Data ingested successfully"}

def test_retrain():
    response = client.post("/retrain")
    assert response.status_code == 200
    assert response.json() == {"message": "Model retrained successfully"}