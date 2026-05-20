# Documentación del Proyecto

## Tecnologías usadas

- Backend: Python, FastAPI, Uvicorn (cuando está disponible), y un servidor HTTP simple como respaldo.
- Cliente de base de datos: Conexión directa a PostgreSQL local utilizando `psycopg2` en `backend/database/db_connection.py`.
- Frontend: Python con PyQt6, vistas basadas en widgets, estilos QSS y componentes personalizados en `frontend/widgets`.
- Dependencias principales: `fastapi`, `uvicorn`, `PyQt6`, `psycopg2`.

## Conexión de la aplicación a la base de datos

La conexión a la base de datos PostgreSQL se realiza en `backend/database/db_connection.py`:

- `load_env()` lee los valores de configuración desde `.env`.
- `DATABASE_URL` obtiene la cadena de conexión de PostgreSQL.
- Se implementan dos funciones principales:
  - `execute_query(query, params)`: para operaciones `SELECT`.
  - `execute_modify(query, params)`: para operaciones `INSERT`, `UPDATE`, `DELETE`.
- Ambas funciones gestionan la conexión usando un bloque `with psycopg2.connect(...)` asegurando que la conexión se cierre correctamente y manejan errores capturando `psycopg2.Error`.

### Variables de entorno clave

- `DATABASE_URL` (Ej: `postgresql://postgres:contraseña@localhost:5432/tarjetas_db`)
- `API_BASE_URL` para el frontend (por defecto `http://127.0.0.1:8000/api`).

## Cómo se hacen las consultas en el backend

El backend está organizado en dos capas:

1. `backend/routes/tarjetas.py`: define las rutas HTTP y expone la API.
2. `backend/services/tarjetas_service.py`: implementa la lógica del negocio ejecutando consultas SQL directas contra PostgreSQL.

### Rutas principales

- `GET /api/health` - salud de la API.
- `GET /api/catalogos` - devuelve catálogos de marcas, líneas, tipos, colores, usos, estados y propietarios.
- `POST /api/catalogos/marca` - crea una nueva marca de vehículo dinámicamente.
- `POST /api/catalogos/linea` - crea una nueva línea de vehículo dinámicamente.
- `POST /api/catalogos/tipo` - crea un nuevo tipo de vehículo dinámicamente.
- `POST /api/catalogos/color` - crea un nuevo color dinámicamente.
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

- `listar_tarjetas()`: utiliza `json_build_object` en SQL para estructurar la respuesta relacional de forma eficiente.
- `catalogos()`: obtiene datos de referencia para formularios.
- `crear_tarjeta(data)`: valida los datos, crea propietario si no existe, crea vehículo y registra la tarjeta con estado `Activa` usando `INSERT ... RETURNING`.
- Funciones `crear_marca`, `crear_linea`, `crear_tipo_vehiculo`, `crear_color`: normalizan entradas usando `.strip().title()` y las insertan en la BD.
- Actualizaciones de mantenimiento (`actualizar_propietario`, `actualizar_motor`, `actualizar_color`): modifican los datos correspondientes e insertan en `historial_cambios`.
- Estados (`desactivar_tarjeta`, `activar_tarjeta`): modifican el `id_estado` de la tarjeta e insertan en `historial_cambios`.
- `eliminar_tarjeta(...)`: elimina en cascada el historial, la tarjeta y el vehículo vinculado.

## Cómo se cargan los datos en el frontend

El frontend usa `frontend/services/api_client.py` para comunicarse con el backend a través de HTTP:

- Llama a los endpoints correspondientes mapeados en `api_client.py`.
- En caso de desconexión, incluye datos de respaldo `demo`.

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
- `frontend/widgets/sidebar.py` renderiza el menú principal (ahora llamado "Registro Vehicular").
- `frontend/widgets/` almacena componentes reutilizables como tarjetas, modales y helpers de UI.
- `frontend/ui/styles.qss` define estilos globales para un diseño moderno (glassmorphism y modo oscuro).

### Validación y Seguridad (Cambios Recientes)

- **Creación de Tarjetas**: `nueva_tarjeta_view.py` incluye validación estricta paso a paso. No se puede avanzar al siguiente paso (Propietario / Tarjeta) si no se han completado correctamente los datos del paso actual.
- **Búsqueda Avanzada**: Incorpora una barra de búsqueda para propietarios a través de NIT.
- **Catálogos Dinámicos**: Los usuarios pueden agregar nuevas marcas, líneas, colores o tipos directamente desde la UI pulsando botones `+`, que despliegan un diálogo de `QInputDialog`.
- **Confirmaciones**: Las acciones críticas como crear tarjeta, cambiar dueños/motor/color, o desactivar tarjetas despliegan un `QMessageBox.question` previniendo errores accidentales.

## Archivos clave

- `backend/database/db_connection.py`
- `backend/services/tarjetas_service.py`
- `backend/routes/tarjetas.py`
- `backend/main.py`
- `frontend/services/api_client.py`
- `frontend/views/nueva_tarjeta_view.py`
- `frontend/views/mantenimiento_view.py`
- `frontend/ui/styles.qss`
- `Docs/db_schema.sql` (Esquema oficial de PostgreSQL)

## Cómo ejecutar el sistema

1. Instalar dependencias desde `requirements.txt` (`pip install -r requirements.txt`).
2. Configurar `.env` con la variable `DATABASE_URL` conectada a tu PostgreSQL local.
3. Asegurarse de que la base de datos PostgreSQL local esté corriendo.
4. Abrir una terminal, entrar a la carpeta principal (`cd Proyecto`) y ejecutar el backend:
   ```bash
   python -m uvicorn backend.main:app --reload
   ```
5. En una segunda terminal, entrar a la carpeta (`cd Proyecto`) y ejecutar el frontend:
   ```bash
   python frontend/main.py
   ```

> Nota: la aplicación frontend consume el backend en `API_BASE_URL`, que por defecto apunta a `http://127.0.0.1:8000/api`.
