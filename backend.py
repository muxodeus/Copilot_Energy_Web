from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime
from time import sleep
import requests
import os
import uvicorn
from databases import Database

# ✅ Correct Database Connection with Async Support
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://mediciones_w63r_user:mJmDFzYPGpwflXHBxmpx8LhxXHAhW2uP@dpg-d17grr95pdvs738che40-a.oregon-postgres.render.com/mediciones_w63r")
database = Database(DATABASE_URL)

# ✅ FastAPI App Initialization
app = FastAPI()

# ✅ CORS for Vue Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Data Model


class DatosMedicion(BaseModel):
    voltaje_A: float
    voltaje_B: float
    voltaje_C: float
    frecuencia: float
    demanda_potencia_activa_total: float
    timestamp: str

# ✅ Auto Insert Data Every 2 Seconds


def modbus_data_loop():
    while True:
        modbus_data = {
            "voltaje_A": 121.5,  # Replace with actual Modbus readings
            "voltaje_B": 123.2,
            "voltaje_C": 119.4,
            "frecuencia": 60.0,
            "demanda_potencia_activa_total": 470.1,
            "timestamp": datetime.utcnow().isoformat()
        }

        response = requests.post(
            "https://copilot-energy-web.onrender.com/recibir_datos",
            json=modbus_data)
        print("Sent Data:", response.json())  # ✅ Debugging

        sleep(2)

# ✅ Startup & Shutdown DB Connection


@app.on_event("startup")
async def check_database_connection():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# ✅ Endpoint to Insert Data


@app.post("/recibir_datos")
async def recibir_datos(datos: DatosMedicion):
    query = """
    INSERT INTO mediciones_w63r (voltaje_a, voltaje_b, voltaje_c, frecuencia, demanda_potencia_activa_total, timestamp)
    VALUES (:voltaje_A, :voltaje_B, :voltaje_C, :frecuencia, :demanda_potencia_activa_total, :timestamp)
    """
    await database.execute(query, datos.dict())
    return {"message": "Datos recibidos correctamente"}

# ✅ Endpoint to Retrieve Data


@app.get("/datos")
async def obtener_datos():
    query = """
    SELECT voltaje_a AS "voltaje_A", voltaje_b AS "voltaje_B", voltaje_c AS "voltaje_C",
           frecuencia, demanda_potencia_activa_total, timestamp
    FROM mediciones_w63r
    ORDER BY timestamp DESC
    LIMIT 50;
    """
    registros = await database.fetch_all(query)

    if not registros:  # ✅ Handle empty response properly
        return {"error": "No data found in database"}

    return [dict(registro) for registro in registros]

    # Confirm FastAPI's Database Connection


@app.get("/check-db")
async def check_database_connection():
    try:
        query = "SELECT NOW() as current_time;"
        result = await database.fetch_one(query)
        return {"status": "Connected", "time": result["current_time"]}
    except Exception as e:
        return {"status": "Error", "details": str(e)}


# ✅ Debug Endpoint to Test DB Connection
@app.get("/debug")
async def debug_query():
    query = "SELECT COUNT(*) AS total_rows FROM mediciones_w63r;"
    result = await database.fetch_one(query)
    return {"Total Records in DB": result["total_rows"]}


# ✅ Run FastAPI with Uvicorn on Render
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
