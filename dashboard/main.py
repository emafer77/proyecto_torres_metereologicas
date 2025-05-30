import streamlit as st
import time
import requests
import pandas as pd

st.title("Torres Meteorológicas")

torres = {
    "torre_Ensenada": "3f9c30d6-1d64-4d47-91e1-4c3ddba5383c",
    "torre_tijuana": "9947f278-6014-4f09-89fc-09d6e3f6c5ab",
    "torre_mexicali": "0b3e9a75-04c6-4de6-bd66-cf5c3cbd5ce0",
    "torre_rosarito": "ffd32590-bc42-4c2f-879f-1364a7e93d2f",
    "torre_tecate": "c15a4da4-e5aa-474d-8e06-2692bb962991"
}
nombre_torres = list(torres.keys())
seleccion = st.selectbox("Selecciona una torre:", nombre_torres)
torre_id = torres[seleccion]



@st.cache_data(ttl=5)
def obtener_datos():
    try:
        res = requests.get("http://127.0.0.1:8000/torres")
        return res.json() if res.status_code == 200 else []
    except Exception as e:
        st.error(f"Error al conectar: {e}")
        return []

def procesar_datos(data):
    return pd.DataFrame([
        {
            "ID": t["identificacion_torre"]["id_torre"],
            "Nombre": t["identificacion_torre"]["nombre"],
            "Estado": t["identificacion_torre"]["estado"],
            "Lat": t["identificacion_torre"]["ubicacion"]["lat"],
            "Lon": t["identificacion_torre"]["ubicacion"]["lon"],
            "Temp": t["datos_meteorologicos"]["temperatura"],
            "Batería": t["datos_tecnicos"]["nivel_bateria"],
            "Estado Sensor": t["datos_tecnicos"]["estado_general"]
        }
        for t in data
    ])

datos = obtener_datos()
if datos:
    df = procesar_datos(datos)
    st.map(df.rename(columns={"Lat": "lat", "Lon": "lon"}))
    st.dataframe(df.drop(columns="ID"), use_container_width=True )
else:
    st.warning("No se pudieron cargar los datos de las torres.")

col1, col2 = st.columns(2)
with col1:
    if st.button("Encender torre"):
        try:
            res = requests.post(f"http://127.0.0.1:8000/torres/{torre_id}/encender")
            if res.status_code == 200:
                st.success(f"Torre '{seleccion}' encendida.")
            else:
                st.error(f"Error: {res.status_code}")
        except Exception as e:
            st.error(f"Error: {e}")

with col2:
    if st.button("Apagar torre"):
        try:
            res = requests.post(f"http://127.0.0.1:8000/torres/{torre_id}/apagar")
            if res.status_code == 200:
                st.success(f"Torre '{seleccion}' apagada.")
            else:
                st.error(f"Error: {res.status_code}")
        except Exception as e:
            st.error(f"Error: {e}")

# 🌀 Toggle para autoactualización
auto = st.checkbox("Activar autoactualización (cada 5 segundos)")
if auto:
    time.sleep(5)
    st.rerun()

