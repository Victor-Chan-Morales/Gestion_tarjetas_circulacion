-- Esquema de base de datos para el proyecto de tarjetas de circulación

CREATE TABLE marca (
    id_marca SERIAL PRIMARY KEY,
    nombre_marca TEXT NOT NULL UNIQUE
);

CREATE TABLE linea (
    id_linea SERIAL PRIMARY KEY,
    id_marca INTEGER NOT NULL REFERENCES marca(id_marca),
    nombre_linea TEXT NOT NULL
);

CREATE TABLE tipo_vehiculo (
    id_tipo SERIAL PRIMARY KEY,
    nombre_tipo TEXT NOT NULL UNIQUE
);

CREATE TABLE color (
    id_color SERIAL PRIMARY KEY,
    nombre_color TEXT NOT NULL UNIQUE
);

CREATE TABLE uso (
    id_uso SERIAL PRIMARY KEY,
    nombre_uso TEXT NOT NULL UNIQUE
);

CREATE TABLE estado (
    id_estado SERIAL PRIMARY KEY,
    nombre_estado TEXT NOT NULL UNIQUE
);

CREATE TABLE propietario (
    id_propietario SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    nit TEXT NOT NULL,
    cui TEXT NOT NULL
);

CREATE TABLE vehiculo (
    vin TEXT PRIMARY KEY,
    placa TEXT NOT NULL UNIQUE,
    id_linea INTEGER NOT NULL REFERENCES linea(id_linea),
    modelo INTEGER NOT NULL,
    id_tipo INTEGER NOT NULL REFERENCES tipo_vehiculo(id_tipo),
    id_color INTEGER NOT NULL REFERENCES color(id_color),
    asientos INTEGER NOT NULL,
    ejes INTEGER NOT NULL,
    cilindros INTEGER NOT NULL,
    cc INTEGER NOT NULL,
    ton NUMERIC DEFAULT 0,
    serie TEXT,
    chasis TEXT,
    motor TEXT NOT NULL
);

CREATE TABLE tarjeta (
    id_tarjeta SERIAL PRIMARY KEY,
    vin TEXT NOT NULL REFERENCES vehiculo(vin),
    id_propietario INTEGER NOT NULL REFERENCES propietario(id_propietario),
    id_uso INTEGER NOT NULL REFERENCES uso(id_uso),
    id_estado INTEGER NOT NULL REFERENCES estado(id_estado),
    codigo_identificador TEXT NOT NULL UNIQUE,
    fecha_registro DATE NOT NULL,
    fecha_emision DATE NOT NULL,
    hora_emision TIME NOT NULL,
    vigencia DATE NOT NULL
);

CREATE TABLE historial_cambios (
    id_historial SERIAL PRIMARY KEY,
    id_tarjeta INTEGER NOT NULL REFERENCES tarjeta(id_tarjeta),
    tipo_cambio TEXT NOT NULL,
    valor_anterior TEXT,
    valor_actual TEXT,
    fecha_cambio TIMESTAMP DEFAULT NOW(),
    observaciones TEXT
);
