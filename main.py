from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
import os

app = FastAPI()

# Crear el directorio 'data' si no existe
os.makedirs('data', exist_ok=True)

# Configurar la base de datos
DATABASE_URL = "sqlite:///./data/test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Definir el modelo de datos
class Advertising(Base):
    __tablename__ = "advertising"
    id = Column(Integer, primary_key=True, index=True)
    TV = Column(Float)
    Radio = Column(Float)
    Newspaper = Column(Float)
    Sales = Column(Float)

Base.metadata.create_all(bind=engine)

# Cargar el modelo
model = None
try:
    model_path = 'data/advertising_model.pkl'
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        print(f"Modelo cargado desde {model_path}")
    else:
        print(f"El archivo {model_path} no existe.")
except Exception as e:
    print(f"Error al cargar el modelo: {e}")

# Pydantic models
class AdData(BaseModel):
    TV: float
    Radio: float
    Newspaper: float

class AdDataIngest(BaseModel):
    TV: float
    Radio: float
    Newspaper: float
    Sales: float

@app.get("/")
def hello():
    return "Hello world"

@app.post("/predict")
def predict(data: List[AdData]):
    if model is None:
        raise HTTPException(status_code=500, detail="Modelo no cargado.")
    
    try:
        df = pd.DataFrame([d.dict() for d in data])
        print("Datos recibidos para predicción:", df)
        predictions = model.predict(df)
        print("Predicciones:", predictions)
        return {"predictions": predictions.tolist()}
    except Exception as e:
        print(f"Error en el endpoint /predict: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest")
def ingest(data: AdDataIngest):
    try:
        db = SessionLocal()
        ad_record = Advertising(TV=data.TV, Radio=data.Radio, Newspaper=data.Newspaper, Sales=data.Sales)
        db.add(ad_record)
        db.commit()
        db.refresh(ad_record)
        return {"message": "Data ingested successfully"}
    except Exception as e:
        print(f"Error en el endpoint /ingest: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/retrain")
def retrain():
    try:
        db = SessionLocal()
        ads = db.query(Advertising).all()
        df = pd.DataFrame([{"TV": ad.TV, "Radio": ad.Radio, "Newspaper": ad.Newspaper, "Sales": ad.Sales} for ad in ads])
        print("Datos recibidos para reentrenamiento:", df)
        X = df[["TV", "Radio", "Newspaper"]]
        y = df["Sales"]
        new_model = LinearRegression()
        new_model.fit(X, y)
        joblib.dump(new_model, 'data/advertising_model.pkl')
        print("Modelo reentrenado y guardado")
        return {"message": "Model retrained successfully"}
    except Exception as e:
        print(f"Error en el endpoint /retrain: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)