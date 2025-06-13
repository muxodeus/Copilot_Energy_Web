from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime
import psycopg2
import os

# Definir la aplicación FastAPI
app = FastAPI()

# Agregar middleware CORS para permitir solicitudes desde localhost:8080
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configura la conexión a PostgreSQL
DATABASE_URL = "postgresql://postgres:gnPxNCofvIzdZXMwvyFpVgRdUJfCBHNO@caboose.proxy.rlwy.net:59649/railway"
conn = psycopg2.connect(DATABASE_URL)

# Modelo de datos
class Medicion(BaseModel):
    voltaje_A: float
    voltaje_B: float
    voltaje_C: float
    frecuencia: float
    demanda_potencia_activa_total: float
    timestamp: datetime = None

# Endpoint para recibir datos (POST)
@app.post("/recibir_datos")
async def recibir_datos(medicion: Medicion):
    try:
        cursor = conn.cursor()
        if not medicion.timestamp:
            medicion.timestamp = datetime.now()
        cursor.execute(
            """
            INSERT INTO mediciones (voltaje_a, voltaje_b, voltaje_c, frecuencia, demanda_potencia_activa_total, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (medicion.voltaje_A, medicion.voltaje_B, medicion.voltaje_C, medicion.frecuencia, medicion.demanda_potencia_activa_total, medicion.timestamp)
        )
        conn.commit()
        cursor.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"mensaje": "Datos almacenados correctamente"}

# Endpoint para obtener datos (GET)
@app.get("/datos", response_model=List[Medicion])
async def obtener_datos():
    try:
        conn.rollback()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT voltaje_a, voltaje_b, voltaje_c, frecuencia, demanda_potencia_activa_total, timestamp
            FROM mediciones
            WHERE timestamp >= NOW() - INTERVAL '30 seconds'
            ORDER BY timestamp ASC
            """
        )
        rows = cursor.fetchall()
        mediciones = [{"voltaje_A": row[0], "voltaje_B": row[1], "voltaje_C": row[2], "frecuencia": row[3], "demanda_potencia_activa_total": row[4], "timestamp": row[5]} for row in rows]
        cursor.close()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    return mediciones
