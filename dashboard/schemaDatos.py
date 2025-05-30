

from datetime import datetime
from uuid import UUID


class DatosAdministrativos:
    fecha_creacion: datetime
    ultima_actualizacion: datetime
    notas: str

    def __init__(self, fecha_creacion: datetime, ultima_actualizacion: datetime, notas: str) -> None:
        self.fecha_creacion = fecha_creacion
        self.ultima_actualizacion = ultima_actualizacion
        self.notas = notas


class DatosMeteorologicos:
    temperatura: float
    humedad_relativa: float
    presion_atmosferica: float
    velocidad_viento: float
    direccion_viento: int
    precipitacion: float
    radiacion_solar: float
    indice_uv: int

    def __init__(self, temperatura: float, humedad_relativa: float, presion_atmosferica: float, velocidad_viento: float, direccion_viento: int, precipitacion: float, radiacion_solar: float, indice_uv: int) -> None:
        self.temperatura = temperatura
        self.humedad_relativa = humedad_relativa
        self.presion_atmosferica = presion_atmosferica
        self.velocidad_viento = velocidad_viento
        self.direccion_viento = direccion_viento
        self.precipitacion = precipitacion
        self.radiacion_solar = radiacion_solar
        self.indice_uv = indice_uv


class DatosTecnicos:
    nivel_bateria: float
    tiempo_ultima_conexion: datetime
    estado_sensor_temperatura: str
    estado_sensor_humedad: str
    estado_general: str

    def __init__(self, nivel_bateria: float, tiempo_ultima_conexion: datetime, estado_sensor_temperatura: str, estado_sensor_humedad: str, estado_general: str) -> None:
        self.nivel_bateria = nivel_bateria
        self.tiempo_ultima_conexion = tiempo_ultima_conexion
        self.estado_sensor_temperatura = estado_sensor_temperatura
        self.estado_sensor_humedad = estado_sensor_humedad
        self.estado_general = estado_general


class Ubicacion:
    lat: float
    lon: float

    def __init__(self, lat: float, lon: float) -> None:
        self.lat = lat
        self.lon = lon


class IdentificacionTorre:
    id_torre: UUID
    nombre: str
    ubicacion: Ubicacion
    usuario_asignado: UUID
    estado: str

    def __init__(self, id_torre: UUID, nombre: str, ubicacion: Ubicacion, usuario_asignado: UUID, estado: str) -> None:
        self.id_torre = id_torre
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.usuario_asignado = usuario_asignado
        self.estado = estado


class TopLevelElement:
    identificacion_torre: IdentificacionTorre
    datos_meteorologicos: DatosMeteorologicos
    datos_tecnicos: DatosTecnicos
    datos_administrativos: DatosAdministrativos

    def __init__(self, identificacion_torre: IdentificacionTorre, datos_meteorologicos: DatosMeteorologicos, datos_tecnicos: DatosTecnicos, datos_administrativos: DatosAdministrativos) -> None:
        self.identificacion_torre = identificacion_torre
        self.datos_meteorologicos = datos_meteorologicos
        self.datos_tecnicos = datos_tecnicos
        self.datos_administrativos = datos_administrativos
