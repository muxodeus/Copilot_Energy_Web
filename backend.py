from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime
import psycopg2
import os
import uvicorn  # Make sure it's imported at the top

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

# Configurar la conexión a PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://mediciones_w63r_user:mJmDFzYPGpwflXHBxmpx8LhxXHAhW2uP@dpg-d17grr95pdvs738che40-a.oregon-postgres.render.com/mediciones_w63r")

try:
    conn = psycopg2.connect(DATABASE_URL)
    print("Database connection successful!")
except psycopg2.OperationalError as e:
    print(f"Error connecting to PostgreSQL: {e}")
    conn = None

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
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection is unavailable.")

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
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection is unavailable.")

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

# Crear la tabla si no existe
if conn is not None:
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mediciones (
            id SERIAL PRIMARY KEY,
            voltaje_a REAL,
            voltaje_b REAL,
            voltaje_c REAL,
            frecuencia REAL,
            demanda_potencia_activa_total REAL,
            timestamp TIMESTAMP DEFAULT NOW()
        );
    """)
    conn.commit()
    cursor.close()

# **Ensure Uvicorn Runs Correctly**
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
