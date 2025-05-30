CREATE TABLE torres (
    id_torre TEXT PRIMARY KEY,  -- UUID como texto
    nombre TEXT NOT NULL,
    ubicacion TEXT,  -- JSON como texto
    usuario_asignado TEXT,  -- UUID como texto, puede ser NULL
    estado TEXT CHECK (estado IN ('Activa', 'Inactiva', 'Falla', 'Mantenimiento'))
);
CREATE TABLE datos_meteorologicos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_torre TEXT,
    temperatura REAL,
    humedad_relativa REAL,
    presion_atmosferica REAL,
    velocidad_viento REAL,
    direccion_viento INTEGER CHECK (direccion_viento BETWEEN 0 AND 360),
    precipitacion REAL,
    radiacion_solar REAL,
    indice_uv INTEGER CHECK (indice_uv BETWEEN 0 AND 11),
    FOREIGN KEY (id_torre) REFERENCES torres(id_torre) ON DELETE CASCADE
);

CREATE TABLE datos_tecnicos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_torre TEXT,
    nivel_bateria REAL CHECK (nivel_bateria BETWEEN 0 AND 100),
    tiempo_ultima_conexion TEXT,  -- Usamos TEXT para timestamps
    estado_sensor_temperatura TEXT CHECK (estado_sensor_temperatura IN ('OK', 'Error')),
    estado_sensor_humedad TEXT CHECK (estado_sensor_humedad IN ('OK', 'Error')),
    estado_general TEXT CHECK (estado_general IN ('Normal', 'Alerta', 'Crítico')),
    FOREIGN KEY (id_torre) REFERENCES torres(id_torre) ON DELETE CASCADE
);
CREATE TABLE datos_administrativos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_torre TEXT,
    fecha_creacion TEXT NOT NULL,  -- TEXT para timestamps
    ultima_actualizacion TEXT,
    notas TEXT,
    origen_datos TEXT CHECK (origen_datos IN ('simulador', 'excel', 'manual')),
    FOREIGN KEY (id_torre) REFERENCES torres(id_torre) ON DELETE CASCADE
);
