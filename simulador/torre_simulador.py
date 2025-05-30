import threading
import random
import time
from datetime import datetime
import sqlite3


datos_en_memoria = {}


# Estados posibles
estados_torre = ["Activa", "Inactiva", "Falla", "Mantenimiento"]
estados_sensor = ["OK", "Error"]
estados_generales = ["Normal", "Alerta", "Crítico"]

# Lista de torres reales
torres_info = [
    {
        "id_torre": "3f9c30d6-1d64-4d47-91e1-4c3ddba5383c",
        "nombre": "torre_ensenada",
        "ubicacion": {"lat": 31.87149, "lon": -116.60071},
        "usuario_asignado": "1c6b917a-8b39-464d-9378-4d94f5d59482"
    },
    {
        "id_torre": "9947f278-6014-4f09-89fc-09d6e3f6c5ab",
        "nombre": "torre_tijuana",
        "ubicacion": {"lat": 32.5027, "lon": -117.0037},
        "usuario_asignado": "27c4c5f3-2ef3-40ea-9a56-d7c3c14aa947"
    },
    {
        "id_torre": "0b3e9a75-04c6-4de6-bd66-cf5c3cbd5ce0",
        "nombre": "torre_mexicali",
        "ubicacion": {"lat": 32.62781, "lon": -115.45446},
        "usuario_asignado": "67b478a4-8464-406e-a0a5-d2954c55e518"
    },
    {
        "id_torre": "ffd32590-bc42-4c2f-879f-1364a7e93d2f",
        "nombre": "torre_rosarito",
        "ubicacion": {"lat": 32.3661011, "lon": -117.0617553},
        "usuario_asignado": "b04ddcb0-42a1-4961-b2f7-b1b92c7d401d"
    },
    {
        "id_torre": "c15a4da4-e5aa-474d-8e06-2692bb962991",
        "nombre": "torre_tecate",
        "ubicacion": {"lat": 32.56717, "lon": -116.62509},
        "usuario_asignado": "f65aa002-2d76-421e-a7ab-8f0edb71ea60"
    }
]

# Guardar en base de datos SQLite
def guardar_en_db(torre_data):
    conn = sqlite3.connect("torres.db")
    cursor = conn.cursor()

    id_info = torre_data["identificacion_torre"]
    meteo = torre_data["datos_meteorologicos"]
    diag = torre_data["datos_tecnicos"]
    admin = torre_data["datos_administrativos"]

    # Tabla torres (REEMPLAZA si ya existe)
    cursor.execute('''
        INSERT OR REPLACE INTO torres (
            id_torre, nombre, latitud, longitud, usuario_asignado, estado
        ) VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        id_info["id_torre"],
        id_info["nombre"],
        id_info["ubicacion"]["lat"],
        id_info["ubicacion"]["lon"],
        id_info["usuario_asignado"],
        id_info["estado"]
    ))

    # Tabla meteorologia (HISTÓRICO)
    cursor.execute('''
        INSERT INTO datos_meteorologicos (
            id_torre, temperatura, humedad_relativa, presion_atmosferica,
            velocidad_viento, direccion_viento, precipitacion,
            radiacion_solar, indice_uv
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        id_info["id_torre"],
        meteo["temperatura"],
        meteo["humedad_relativa"],
        meteo["presion_atmosferica"],
        meteo["velocidad_viento"],
        meteo["direccion_viento"],
        meteo["precipitacion"],
        meteo["radiacion_solar"],
        meteo["indice_uv"],
        
    ))

    # Tabla diagnostico
    cursor.execute('''
        INSERT INTO datos_tecnicos (
            id_torre, nivel_bateria, tiempo_ultima_conexion,
            estado_sensor_temperatura, estado_sensor_humedad, estado_general
        ) VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        id_info["id_torre"],
        diag["nivel_bateria"],
        diag["tiempo_ultima_conexion"],
        diag["estado_sensor_temperatura"],
        diag["estado_sensor_humedad"],
        diag["estado_general"]
    ))

    # Tabla administracion
    cursor.execute('''
        INSERT INTO datos_administrativos (
            id_torre, fecha_creacion, ultima_actualizacion, notas
        ) VALUES (?, ?, ?, ?)
    ''', (
        id_info["id_torre"],
        admin["fecha_creacion"],
        admin["ultima_actualizacion"],
        admin["notas"]
    ))

    conn.commit()
    conn.close()



class TorreMeteorologicaThread(threading.Thread):
    def __init__(self, torre):
        super().__init__()
        self.torre = torre
        self.encendida = threading.Event()
        self.detener = threading.Event()

    def run(self):
        print(f"[{self.torre['nombre']}] Hilo iniciado.")
        while not self.detener.is_set():
            if self.encendida.is_set():
                self.generar_y_guardar_datos()
                time.sleep(2)
            else:
                time.sleep(1)

    def generar_y_guardar_datos(self):
        now = datetime.utcnow().isoformat()

        torre_data = {
            "identificacion_torre": {
                "id_torre": self.torre["id_torre"],
                "nombre": self.torre["nombre"],
                "ubicacion": self.torre["ubicacion"],
                "usuario_asignado": self.torre["usuario_asignado"],
                "estado": random.choice(estados_torre)
            },
            "datos_meteorologicos": {
                "temperatura": round(random.uniform(-10, 45), 2),
                "humedad_relativa": round(random.uniform(10, 100), 2),
                "presion_atmosferica": round(random.uniform(950, 1050), 2),
                "velocidad_viento": round(random.uniform(0, 30), 2),
                "direccion_viento": random.randint(0, 360),
                "precipitacion": round(random.uniform(0, 20), 2),
                "radiacion_solar": round(random.uniform(0, 1200), 2),
                "indice_uv": random.randint(0, 11)
            },
            "datos_tecnicos": {
                "nivel_bateria": round(random.uniform(0, 100), 2),
                "tiempo_ultima_conexion": now,
                "estado_sensor_temperatura": random.choice(estados_sensor),
                "estado_sensor_humedad": random.choice(estados_sensor),
                "estado_general": random.choice(estados_generales)
            },
            "datos_administrativos": {
                "fecha_creacion": now,
                "ultima_actualizacion": now,
                "notas": "Simulación automática de datos."
            }
        }

        try:
            guardar_en_db(torre_data)
        except Exception as e:
            print(f" Error SQLite ({self.torre['nombre']}): {e}")
        try:
            guardar_en_supabase(torre_data)
        except Exception as e:
            print(f" Error Supabase ({self.torre['nombre']}): {e}")

        torre_data["identificacion_torre"]["activa"] = self.encendida.is_set()
        datos_en_memoria[self.torre["id_torre"]] = torre_data

        print(f"[{self.torre['nombre']}] Datos guardados.")

    def encender(self):
        print(f"[{self.torre['nombre']}] Encendida.")
        self.encendida.set()

    def apagar(self):
        print(f"[{self.torre['nombre']}] Apagada.")
        self.encendida.clear()

    def terminar(self):
        print(f"[{self.torre['nombre']}] Terminando hilo.")
        self.detener.set()
        self.encendida.set()  # Desbloquea si estaba esperando

      
from supabase import create_client, Client


import os
from dotenv import load_dotenv

 # Cargar el archivo .env
load_dotenv()

 # Obtener las variables
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def guardar_en_supabase(torre_data):
    id_info = torre_data["identificacion_torre"]
    meteo = torre_data["datos_meteorologicos"]
    diag = torre_data["datos_tecnicos"]
    admin = torre_data["datos_administrativos"]

    supabase.table("torres").upsert({
        "id_torre": id_info["id_torre"],
        "nombre": id_info["nombre"],
        "latitud": id_info["ubicacion"]["lat"],
        "longitud": id_info["ubicacion"]["lon"],
        "usuario_asignado": id_info["usuario_asignado"],
        "estado": id_info["estado"]
    }).execute()

    supabase.table("datos_meteorologicos").insert({
        "id_torre": id_info["id_torre"],
        "temperatura": meteo["temperatura"],
        "humedad_relativa": meteo["humedad_relativa"],
        "presion_atmosferica": meteo["presion_atmosferica"],
        "velocidad_viento": meteo["velocidad_viento"],
        "direccion_viento": meteo["direccion_viento"],
        "precipitacion": meteo["precipitacion"],
        "radiacion_solar": meteo["radiacion_solar"],
        "indice_uv": meteo["indice_uv"]
    }).execute()

    supabase.table("datos_tecnicos").insert({
        "id_torre": id_info["id_torre"],
        "nivel_bateria": diag["nivel_bateria"],
        "tiempo_ultima_conexion": diag["tiempo_ultima_conexion"],
        "estado_sensor_temperatura": diag["estado_sensor_temperatura"],
        "estado_sensor_humedad": diag["estado_sensor_humedad"],
        "estado_general": diag["estado_general"]
    }).execute()

    supabase.table("datos_administrativos").insert({
        "id_torre": id_info["id_torre"],
        "fecha_creacion": admin["fecha_creacion"],
        "ultima_actualizacion": admin["ultima_actualizacion"],
        "notas": admin["notas"]
    }).execute()

    print(f"Datos enviados a Supabase para {id_info['nombre']}")

# Diccionario global de hilos
torres_threads = {t["id_torre"]: TorreMeteorologicaThread(t) for t in torres_info}


