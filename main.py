from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression

app = FastAPI()

# Configurar la base de datos
DATABASE_URL = "sqlite:///./data/test.db"
engine = create_engine(DATABASE_URL)
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
model = joblib.load('data/advertising_model.pkl')

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

@app.post("/predict")
def predict(data: List[AdData]):
    df = pd.DataFrame([d.dict() for d in data])
    predictions = model.predict(df)
    return {"predictions": predictions.tolist()}

@app.post("/ingest")
def ingest(data: AdDataIngest):
    db = SessionLocal()
    ad_record = Advertising(TV=data.TV, Radio=data.Radio, Newspaper=data.Newspaper, Sales=data.Sales)
    db.add(ad_record)
    db.commit()
    db.refresh(ad_record)
    return {"message": "Data ingested successfully"}

@app.post("/retrain")
def retrain():
    db = SessionLocal()
    ads = db.query(Advertising).all()
    df = pd.DataFrame([{"TV": ad.TV, "Radio": ad.Radio, "Newspaper": ad.Newspaper, "Sales": ad.Sales} for ad in ads])
    X = df[["TV", "Radio", "Newspaper"]]
    y = df["Sales"]
    new_model = LinearRegression()
    new_model.fit(X, y)
    joblib.dump(new_model, 'data/advertising_model.pkl')
    return {"message": "Model retrained successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
