-- Datos iniciales 

-- Catalogos
INSERT INTO marca (nombre_marca) VALUES
('Toyota'), ('Honda'), ('Nissan'), ('Mazda'), ('Chevrolet'), ('Ford'), ('Hyundai')
ON CONFLICT (nombre_marca) DO NOTHING;

INSERT INTO tipo_vehiculo (nombre_tipo) VALUES
('Sedan'), ('Pick Up'), ('SUV'), ('Hatchback')
ON CONFLICT (nombre_tipo) DO NOTHING;

INSERT INTO color (nombre_color) VALUES
('Blanco'), ('Negro'), ('Gris'), ('Rojo'), ('Azul'), ('Plata'), ('Verde')
ON CONFLICT (nombre_color) DO NOTHING;

INSERT INTO uso (nombre_uso) VALUES
('Particular'), ('Comercial')
ON CONFLICT (nombre_uso) DO NOTHING;

INSERT INTO estado (nombre_estado) VALUES
('Activa'), ('Inactiva'), ('Suspendida'), ('Vencida')
ON CONFLICT (nombre_estado) DO NOTHING;

INSERT INTO linea (id_marca, nombre_linea)
SELECT m.id_marca, v.nombre_linea
FROM (VALUES
  ('Toyota', 'Corolla'),
  ('Toyota', 'Hilux'),
  ('Honda', 'Civic'),
  ('Nissan', 'Sentra'),
  ('Mazda', 'CX-5'),
  ('Chevrolet', 'Spark'),
  ('Ford', 'Ranger'),
  ('Hyundai', 'Tucson')
) AS v(nombre_marca, nombre_linea)
JOIN marca m ON m.nombre_marca = v.nombre_marca
WHERE NOT EXISTS (
  SELECT 1 FROM linea l
  WHERE l.id_marca = m.id_marca AND l.nombre_linea = v.nombre_linea
);

-- Propietarios
INSERT INTO propietario (nombre, nit, cui) VALUES
('Juan Carlos Perez Lopez', '1234567-8', '1234567890101'),
('Maria Elena Garcia Morales', '8765432-1', '8765432101234'),
('Carlos Roberto Martinez', '5678901-2', '2345678901234'),
('Ana Lucia Hernandez Ruiz', '9012345-6', '3456789012345'),
('Pedro Antonio Ramirez', '3456789-0', '4567890123456'),
('Sofia Alejandra Cruz', '7890123-4', '5678901234567'),
('Miguel Angel Flores', '2345678-9', '6789012345678'),
('Laura Patricia Mendez', '6789012-3', '7890123456789')
ON CONFLICT (nit) DO NOTHING;

-- Vehiculos
INSERT INTO vehiculo (
  vin, placa, id_linea, modelo, id_tipo, id_color,
  asientos, ejes, cilindros, cc, ton, serie, chasis, motor
)
SELECT *
FROM (
  VALUES
  ('JTDKN3DU5A0123456', 'P-123ABC', 'Toyota', 'Corolla', 2022, 'Sedan', 'Blanco', 5, 2, 4, 1800, 0.00, 'SER001', 'CHS001', 'MOT001'),
  ('8AJBA3CD9P0123456', 'P-456DEF', 'Toyota', 'Hilux', 2023, 'Pick Up', 'Negro', 5, 2, 4, 2400, 1.05, 'SER002', 'CHS002', 'MOT002'),
  ('2HGFB2F59CH123456', 'P-789GHI', 'Honda', 'Civic', 2021, 'Sedan', 'Gris', 5, 2, 4, 1800, 0.00, 'SER003', 'CHS003', 'MOT003'),
  ('3N1AB7AP8HY123456', 'P-012JKL', 'Nissan', 'Sentra', 2020, 'Sedan', 'Rojo', 5, 2, 4, 1600, 0.00, 'SER004', 'CHS004', 'MOT004'),
  ('JM3KE2CY0G0123456', 'P-345MNO', 'Mazda', 'CX-5', 2024, 'SUV', 'Azul', 5, 2, 4, 2000, 0.00, 'SER005', 'CHS005', 'MOT005'),
  ('KL1MJ6C33HC123456', 'P-678PQR', 'Chevrolet', 'Spark', 2019, 'Hatchback', 'Verde', 5, 2, 4, 1200, 0.00, 'SER006', 'CHS006', 'MOT006'),
  ('1FTER4FH5NLD12345', 'C-901STU', 'Ford', 'Ranger', 2022, 'Pick Up', 'Plata', 5, 2, 4, 2500, 1.20, 'SER007', 'CHS007', 'MOT007'),
  ('KM8J3CAL6PU123456', 'P-234VWX', 'Hyundai', 'Tucson', 2023, 'SUV', 'Blanco', 5, 2, 4, 2000, 0.00, 'SER008', 'CHS008', 'MOT008')
) AS v(vin, placa, marca, linea, modelo, tipo, color, asientos, ejes, cilindros, cc, ton, serie, chasis, motor)
JOIN marca m ON m.nombre_marca = v.marca
JOIN linea l ON l.id_marca = m.id_marca AND l.nombre_linea = v.linea
JOIN tipo_vehiculo tv ON tv.nombre_tipo = v.tipo
JOIN color c ON c.nombre_color = v.color
WHERE NOT EXISTS (SELECT 1 FROM vehiculo x WHERE x.vin = v.vin);

-- Tarjetas
INSERT INTO tarjeta (
  vin, id_propietario, id_uso, id_estado,
  codigo_identificador, fecha_registro, fecha_emision, hora_emision, vigencia
)
SELECT v.vin, p.id_propietario, u.id_uso, e.id_estado,
       d.codigo, d.fecha_registro::date, d.fecha_emision::date, d.hora_emision::time, d.vigencia::date
FROM (
  VALUES
  ('TC-2024-000001', 'JTDKN3DU5A0123456', '1234567-8', 'Particular', 'Activa', '2024-01-15', '2024-01-15', '09:30:00', '2025-01-15'),
  ('TC-2024-000002', '8AJBA3CD9P0123456', '8765432-1', 'Comercial', 'Activa', '2024-02-20', '2024-02-20', '10:15:00', '2025-02-20'),
  ('TC-2024-000003', '2HGFB2F59CH123456', '5678901-2', 'Particular', 'Inactiva', '2024-03-10', '2024-03-10', '11:00:00', '2025-03-10'),
  ('TC-2023-000045', '3N1AB7AP8HY123456', '9012345-6', 'Particular', 'Vencida', '2023-06-05', '2023-06-05', '08:45:00', '2024-06-05'),
  ('TC-2024-000010', 'JM3KE2CY0G0123456', '3456789-0', 'Particular', 'Activa', '2024-04-12', '2024-04-12', '13:20:00', '2025-04-12'),
  ('TC-2024-000015', 'KL1MJ6C33HC123456', '7890123-4', 'Particular', 'Suspendida', '2024-05-08', '2024-05-08', '14:10:00', '2025-05-08'),
  ('TC-2024-000020', '1FTER4FH5NLD12345', '2345678-9', 'Comercial', 'Activa', '2024-06-15', '2024-06-15', '15:00:00', '2025-06-15'),
  ('TC-2024-000025', 'KM8J3CAL6PU123456', '6789012-3', 'Particular', 'Activa', '2024-07-22', '2024-07-22', '16:25:00', '2025-07-22')
) AS d(codigo, vin, nit, uso, estado, fecha_registro, fecha_emision, hora_emision, vigencia)
JOIN vehiculo v ON v.vin = d.vin
JOIN propietario p ON p.nit = d.nit
JOIN uso u ON u.nombre_uso = d.uso
JOIN estado e ON e.nombre_estado = d.estado
WHERE NOT EXISTS (SELECT 1 FROM tarjeta t WHERE t.codigo_identificador = d.codigo);


-- Historial
INSERT INTO historial_cambios (
  id_tarjeta, tipo_cambio, valor_anterior, valor_actual, fecha_cambio, observaciones
)
SELECT t.id_tarjeta, h.tipo_cambio, h.valor_anterior, h.valor_actual, h.fecha_cambio::timestamp, h.observaciones
FROM (
  VALUES
  ('TC-2024-000001', 'CAMBIO COLOR', 'Gris', 'Blanco', '2024-03-15 10:20:00', 'Cambio de color autorizado.'),
  ('TC-2024-000002', 'CAMBIO MOTOR', 'MOT-OLD-002', 'MOT002', '2024-04-20 12:10:00', 'Reemplazo de motor por falla mecanica.'),
  ('TC-2024-000010', 'CAMBIO DUENO', 'Carlos Martinez', 'Pedro Antonio Ramirez', '2024-05-10 09:00:00', 'Traspaso de vehiculo autorizado.')
) AS h(codigo, tipo_cambio, valor_anterior, valor_actual, fecha_cambio, observaciones)
JOIN tarjeta t ON t.codigo_identificador = h.codigo
WHERE NOT EXISTS (
  SELECT 1 FROM historial_cambios hc
  WHERE hc.id_tarjeta = t.id_tarjeta
    AND hc.tipo_cambio = h.tipo_cambio
    AND hc.fecha_cambio = h.fecha_cambio::timestamp
);
