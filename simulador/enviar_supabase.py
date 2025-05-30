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
    try:
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

        print(f"✅ Datos enviados a Supabase para {id_info['nombre']}")
    except Exception as e:
        print(f"⚠️ Error al enviar datos a Supabase para {torre_data['identificacion_torre']['nombre']}: {e}")
