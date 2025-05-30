CREATE TABLE torres (
    id_torre UUID PRIMARY KEY,  -- o puedes usar SERIAL o BIGINT si prefieres int
    nombre TEXT NOT NULL,
    ubicacion JSONB,  -- También puedes usar TEXT si es solo una dirección
    usuario_asignado UUID,  -- NULL si no hay usuario asignado
    estado TEXT CHECK (estado IN ('Activa', 'Inactiva', 'Falla', 'Mantenimiento'))
);

CREATE TABLE datos_meteorologicos (
    id SERIAL PRIMARY KEY,
    id_torre UUID REFERENCES torres(id_torre) ON DELETE CASCADE,
    temperatura FLOAT,
    humedad_relativa FLOAT,
    presion_atmosferica FLOAT,
    velocidad_viento FLOAT,
    direccion_viento INT CHECK (direccion_viento BETWEEN 0 AND 360),
    precipitacion FLOAT,
    radiacion_solar FLOAT,
    indice_uv INT CHECK (indice_uv BETWEEN 0 AND 11)
);

CREATE TABLE datos_tecnicos (
    id SERIAL PRIMARY KEY,
    id_torre UUID REFERENCES torres(id_torre) ON DELETE CASCADE,
    nivel_bateria FLOAT CHECK (nivel_bateria BETWEEN 0 AND 100),
    tiempo_ultima_conexion TIMESTAMP,
    estado_sensor_temperatura TEXT CHECK (estado_sensor_temperatura IN ('OK', 'Error')),
    estado_sensor_humedad TEXT CHECK (estado_sensor_humedad IN ('OK', 'Error')),
    estado_general TEXT CHECK (estado_general IN ('Normal', 'Alerta', 'Crítico'))
);

CREATE TABLE datos_administrativos (
    id SERIAL PRIMARY KEY,
    id_torre UUID REFERENCES torres(id_torre) ON DELETE CASCADE,
    fecha_creacion TIMESTAMP NOT NULL,
    ultima_actualizacion TIMESTAMP,
    notas TEXT,
    origen_datos TEXT CHECK (origen_datos IN ('simulador', 'excel', 'manual'))
);