from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from simulador.torre_simulador import torres_threads, datos_en_memoria

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicialización: se ejecuta al arrancar
    for thread in torres_threads.values():
        thread.start()
    print("🌀 Simulación iniciada")
    yield
    # Finalización: aquí podrías hacer limpieza si fuera necesario
    print("🚪 Simulación finalizada")

app = FastAPI(lifespan=lifespan)

@app.get("/torres")
def obtener_torres():
    return [
        torre for torre in datos_en_memoria.values()
        if torre["identificacion_torre"].get("activa", True)
    ]

@app.post("/torres/{id_torre}/encender")
def encender_torre(id_torre: str):
    torre = torres_threads.get(id_torre)
    if torre is None:
        raise HTTPException(status_code=404, detail="Torre no encontrada")
    torre.encender()
    return {"mensaje": f"Torre {id_torre} encendida"}

@app.post("/torres/{id_torre}/apagar")
def apagar_torre(id_torre: str):
    torre = torres_threads.get(id_torre)
    if torre is None:
        raise HTTPException(status_code=404, detail="Torre no encontrada")
    torre.apagar()
    return {"mensaje": f"Torre {id_torre} apagada"}

@app.get("/torres/{id_torre}/estado")
def estado_torre(id_torre: str):
    torre = torres_threads.get(id_torre)
    if torre is None:
        raise HTTPException(status_code=404, detail="Torre no encontrada")
    estado = "encendida" if torre.encendida.is_set() else "apagada"
    return {"estado": estado}
