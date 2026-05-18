# Documentación del Proyecto

## Tecnologías usadas

- Backend: Python, FastAPI, Uvicorn (cuando está disponible), y un servidor HTTP simple como respaldo.
- Cliente de base de datos: Supabase REST API utilizando `urllib.request` en `backend/database/supabase_client.py`.
- Frontend: Python con PyQt6, vistas basadas en widgets, estilos QSS y componentes personalizados en `frontend/widgets`.
- Dependencias principales: `fastapi`, `uvicorn`, `PyQt6` y algunos paquetes estándar de Python.

## Conexión de la aplicación a la base de datos

La conexión a la base de datos Supabase se realiza en `backend/database/supabase_client.py`:

- `load_env()` lee los valores de configuración desde `.env`.
- `SUPABASE_URL` obtiene la URL del proyecto Supabase.
- `SUPABASE_KEY` toma la clave de servicio o la clave anónima disponible.
- La función `request(table, method, select, filters, payload, prefer)` construye la URL REST de Supabase y define encabezados adecuados.
- Se utiliza `urllib.request.urlopen` para ejecutar los pedidos HTTP y parsear la respuesta JSON.
- Se maneja la respuesta de error con `SupabaseError` y se traducen mensajes de fallo en texto legible.

### Variables de entorno clave

- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY` o `SUPABASE_KEY`
- `API_BASE_URL` para el frontend cuando se usa el cliente HTTP con la API local.

## Cómo se hacen las consultas en el backend

El backend está organizado en dos capas:

1. `backend/routes/tarjetas.py`: define las rutas HTTP y expone la API.
2. `backend/services/tarjetas_service.py`: implementa la lógica del negocio y las consultas a Supabase.

### Rutas principales

- `GET /api/health` - salud de la API.
- `GET /api/catalogos` - devuelve catálogos de marcas, líneas, tipos, colores, usos, estados y propietarios.
- `GET /api/tarjetas` - devuelve todas las tarjetas con los datos relacionados de vehículo, propietario, uso y estado.
- `POST /api/tarjetas` - crea una nueva tarjeta y el vehículo asociado.
- `POST /api/mantenimiento/dueno` - actualiza el propietario de la tarjeta.
- `POST /api/mantenimiento/motor` - registra un cambio de motor y actualiza el vehículo.
- `POST /api/mantenimiento/color` - registra un cambio de color y actualiza el vehículo.
- `POST /api/mantenimiento/activar` - reactivación de una tarjeta desde mantenimiento.
- `POST /api/desactivaciones` - desactiva una tarjeta.
- `GET /api/historial` - lista el historial de cambios.
- `DELETE /api/tarjetas/{id_tarjeta}` - elimina una tarjeta y su vehículo asociado.

### Lógica de servicios

En `backend/services/tarjetas_service.py` se maneja:

- `listar_tarjetas()`: consulta la tabla `tarjeta` con joins a `vehiculo`, `propietario`, `uso` y `estado`.
- `catalogos()`: obtiene datos de referencia para formularios.
- `crear_tarjeta(data)`: valida los datos, crea propietario si no existe, crea vehículo y registra la tarjeta con estado `Activa`.
- `actualizar_propietario(...)`: cambia el propietario de una tarjeta y crea un registro de historial.
- `actualizar_motor(...)`: actualiza campos del vehículo y crea el historial del cambio.
- `actualizar_color(...)`: actualiza el color del vehículo y registra el historial.
- `desactivar_tarjeta(...)`: actualiza el estado de la tarjeta a `Inactiva` y escribe el historial.
- `activar_tarjeta(...)`: actualiza la tarjeta a estado `Activa` y registra la reactivación en el historial.
- `listar_historial()`: obtiene el historial de cambios con la tarjeta y la placa asociada.
- `eliminar_tarjeta(...)`: elimina el historial, la tarjeta y el vehículo vinculado.

## Cómo se cargan los datos en el frontend

El frontend usa `frontend/services/api_client.py` para comunicarse con el backend a través de HTTP:

- `obtener_tarjetas()` llama a `/tarjetas`.
- `obtener_catalogos()` llama a `/catalogos`.
- `crear_tarjeta(payload)` llama a `/tarjetas`.
- `registrar_cambio_dueno(payload)` llama a `/mantenimiento/dueno`.
- `registrar_cambio_motor(payload)` llama a `/mantenimiento/motor`.
- `registrar_cambio_color(payload)` llama a `/mantenimiento/color`.
- `reactivar_tarjeta(payload)` llama a `/mantenimiento/activar`.
- `desactivar_tarjeta(payload)` llama a `/desactivaciones`.
- `obtener_historial()` llama a `/historial`.
- `eliminar_tarjeta(id_tarjeta)` llama a `/tarjetas/{id_tarjeta}`.

El cliente también incluye datos de respaldo `demo` cuando el backend no responde.

## Cómo funciona el backend detalladamente

### Inicialización

- `backend/main.py` intenta usar FastAPI y, si no está disponible, cae en un servidor HTTP simple.
- Cuando FastAPI está disponible, se monta `backend/routes/tarjetas` en el prefijo `/api`.
- El servidor HTTP alternativo expone las mismas rutas básicas para crear, actualizar y consultar datos.

### Flujo de creación de tarjeta

1. El frontend envía un POST a `/api/tarjetas` con los datos del vehículo y propietario.
2. `tarjetas_service.crear_tarjeta` valida la información.
3. Si el propietario no existe, lo crea en la tabla `propietario`.
4. Crea el registro en `vehiculo` con `vin`, `placa`, `motor`, color y características.
5. Inserta el registro en `tarjeta` con estado `Activa` y fechas de emisión y vigencia.

### Cambios de mantenimiento

- `mantenimiento/dueno`: actualiza `id_propietario` en `tarjeta`.
- `mantenimiento/motor`: actualiza `vehiculo.motor`, `cilindros` y `cc`.
- `mantenimiento/color`: actualiza `vehiculo.id_color`.
- `mantenimiento/activar`: actualiza `tarjeta.id_estado` a `Activa`.

### Registro en historial

Cada acción importante genera un registro en `historial_cambios`, incluyendo:
- `id_tarjeta`
- `tipo_cambio`
- `valor_anterior`
- `valor_actual`
- `observaciones`

## Cómo funciona el frontend detalladamente

### Estructura general

- `frontend/main.py` inicializa la aplicación PyQt6.
- `frontend/views/` contiene vistas de cada pantalla:
  - `dashboard_view.py`
  - `tarjetas_view.py`
  - `historial_view.py`
  - `desactivaciones_view.py`
  - `mantenimiento_view.py`
  - `nueva_tarjeta_view.py`
- `frontend/widgets/` almacena componentes reutilizables como tarjetas, modales, barras laterales y helpers de UI.
- `frontend/ui/styles.qss` define estilos globales.

### Vista de mantenimiento

- Presenta una lista de tarjetas disponibles.
- Permite cambiar propietario, motor o color.
- Muestra un botón de `Reactivar tarjeta` cuando la tarjeta seleccionada no está activa.
- Llama a la API `/mantenimiento/activar` para que el backend actualice el estado y registre el historial.

### Comportamiento visual

- El tema usa colores oscuros y botones con contraste moderado.
- Los componentes reutilizan funciones de `widgets/ui_helpers.py` como `card()`, `badge()`, `input_field()` y `primary_button()`.

## Archivos clave

- `backend/database/supabase_client.py`
- `backend/services/tarjetas_service.py`
- `backend/routes/tarjetas.py`
- `backend/main.py`
- `frontend/services/api_client.py`
- `frontend/views/mantenimiento_view.py`
- `frontend/ui/styles.qss`
- `Docs/seed_datos_supabase.sql`

## Cambios recientes realizados

- Se agregó la acción de reactivación en backend: `tarjetas_service.activar_tarjeta()`.
- Se expuso la ruta `POST /api/mantenimiento/activar`.
- Se añadió soporte para esta ruta también en el servidor HTTP alternativo.
- Se integró un botón `Reactivar tarjeta` en `frontend/views/mantenimiento_view.py`.
- Se creó `Docs/db_schema.sql` con los scripts de creación de tablas.

## Cómo ejecutar el sistema

1. Instalar dependencias desde `requirements.txt`.
2. Configurar `.env` con `SUPABASE_URL` y `SUPABASE_SERVICE_ROLE_KEY` o `SUPABASE_KEY`.
3. Ejecutar el backend con `python backend/main.py` o usando FastAPI si está instalado.
4. Ejecutar el frontend con `python frontend/main.py`.

> Nota: la aplicación frontend consume el backend en `API_BASE_URL`, que por defecto apunta a `http://127.0.0.1:8000/api`.
