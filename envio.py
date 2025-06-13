import requests
from pymodbus.client import ModbusTcpClient
import struct
import time
import random

# Configuración del cliente Modbus con timeout de 2 segundos.
MODBUS_IP = "192.168.86.205"
MODBUS_PORT = 502
client = ModbusTcpClient(MODBUS_IP, port=MODBUS_PORT, timeout=2)

# Intentamos conectar solo una vez al inicio.
if not client.connect():
    print("❌ No se pudo conectar al medidor Modbus TCP")
    exit(1)
else:
    print("✅ Conexión establecida con el medidor Modbus TCP")

# URL del backend (endpoint que recibe datos)
CLOUD_API_URL = "http://localhost:8000/recibir_datos"

# Diccionario de parámetros con las direcciones Modbus originales.
PARAMETROS = {
    "voltaje_A": 41010,
    "voltaje_B": 41012,
    "voltaje_C": 41014,
    "voltaje_AB": 41020,
    "voltaje_BC": 41022,
    "voltaje_CA": 41024,
    "corriente_A": 41000,
    "corriente_B": 41002,
    "corriente_C": 41004,
    "potencia_activa_A": 41028,
    "potencia_activa_B": 41030,
    "potencia_activa_C": 41032,
    "potencia_activa_total": 41034,
    "potencia_reactiva_A": 41036,
    "potencia_reactiva_B": 41038,
    "potencia_reactiva_C": 41040,
    "potencia_reactiva_total": 41042,
    "potencia_aparente_A": 41044,
    "potencia_aparente_B": 41046,
    "potencia_aparente_C": 41048,
    "potencia_aparente_total": 41050,
    "factor_potencia_A": 41052,
    "factor_potencia_B": 41054,
    "factor_potencia_C": 41056,
    "factor_potencia_promedio": 41058,
    "energia_importada_A": 42600,
    "energia_importada_B": 42602,
    "energia_importada_C": 42604,
    "energia_importada_total": 42606,
    "energia_exportada_A": 42608,
    "energia_exportada_B": 42610,
    "energia_exportada_C": 42612,
    "energia_exportada_total": 42614,
    "distorsion_armonica_voltaje_A": 45000,
    "distorsion_armonica_voltaje_B": 45002,
    "distorsion_armonica_voltaje_C": 45004,
    "distorsion_armonica_corriente_A": 44000,
    "distorsion_armonica_corriente_B": 44002,
    "distorsion_armonica_corriente_C": 44004,
    "frecuencia": 41074,
    "demanda_potencia_activa_total": 43046
}

# Ajuste de direcciones a base 0 para pymodbus (se resta 40001)
for key in PARAMETROS:
    PARAMETROS[key] -= 40001

def leer_parametro(nombre, direccion):
    try:
        # Si deseas simular datos para "voltaje_A", descomenta las siguientes líneas:
        # if nombre == "voltaje_A":
        #     return round(random.uniform(110, 130), 2)
        lectura = client.read_holding_registers(direccion, count=2)
        if lectura.isError():
            print(f"❌ Error en lectura Modbus para {nombre}")
            return None
        raw_bytes = struct.pack("<HH", lectura.registers[0], lectura.registers[1])
        valor = struct.unpack("<f", raw_bytes)[0]
        return valor
    except Exception as e:
        print(f"❌ Error inesperado en {nombre}: {e}")
        return None

def leer_todos_los_parametros():
    datos = {}
    for nombre, direccion in PARAMETROS.items():
        if nombre == "voltaje_A":
            # Simulación para variar "voltaje_A"
            datos[nombre] = round(random.uniform(110, 130), 2)
        else:
            datos[nombre] = leer_parametro(nombre, direccion)
    return datos

def enviar_a_nube(datos):
    try:
        response = requests.post(CLOUD_API_URL, json=datos)
        if response.status_code == 200:
            print("✅ Datos enviados correctamente a la nube")
        else:
            print(f"❌ Error al enviar datos: {response.status_code}")
    except Exception as e:
        print(f"❌ Error en envío a la nube: {e}")

# Bucle principal: intenta realizar cada ciclo en 2 segundos en total.
while True:
    inicio = time.time()
    print("\n--- Inicio del ciclo ---", time.strftime("%H:%M:%S"))
    
    datos_medidor = leer_todos_los_parametros()
    if datos_medidor:
        enviar_a_nube(datos_medidor)
    
    fin = time.time()
    duracion = fin - inicio
    print(f"Ciclo completado en: {duracion:.2f} segundos")
    tiempo_espera = max(2.0 - duracion, 0)
    print(f"Esperando: {tiempo_espera:.2f} segundos para el siguiente ciclo")
    time.sleep(tiempo_espera)
