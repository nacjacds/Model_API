from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
import os
import uvicorn

app = FastAPI()

# Crear el directorio 'data' si no existe
os.makedirs('data', exist_ok=True)

# Configurar la base de datos
conn = sqlite3.connect('data/test.db', check_same_thread=False)
cursor = conn.cursor()

# Crear la tabla si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS advertising (
    id INTEGER PRIMARY KEY,
    TV FLOAT,
    Radio FLOAT,
    Newspaper FLOAT,
    Sales FLOAT
)
''')
conn.commit()

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
def predict(data: list[AdData]):
    global model
    if model is None:
        raise HTTPException(status_code=500, detail="Modelo no cargado.")
    try:
        df = pd.DataFrame([d.dict() for d in data])
        print("Datos recibidos para predicción:", df)
        df.columns = ['TV', 'Radio', 'Newspaper']  # Asegurarse de que las columnas coincidan
        predictions = model.predict(df)
        print("Predicciones:", predictions)
        return {"predictions": predictions.tolist()}
    except Exception as e:
        print(f"Error en el endpoint /predict: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest")
def ingest(data: AdDataIngest):
    try:
        cursor.execute(
            "INSERT INTO advertising (TV, Radio, Newspaper, Sales) VALUES (?, ?, ?, ?)",
            (data.TV, data.Radio, data.Newspaper, data.Sales)
        )
        conn.commit()
        return {"message": "Data ingested successfully"}
    except Exception as e:
        print(f"Error en el endpoint /ingest: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/retrain")
def retrain():
    try:
        cursor.execute("SELECT TV, Radio, Newspaper, Sales FROM advertising")
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=["TV", "Radio", "Newspaper", "Sales"])
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
    uvicorn.run(app, host="127.0.0.1", port=8000)