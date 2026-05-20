# Gestor de Tarjetas de Circulación

Bienvenido, este es un proyecto del curso de Base de datos 1, el cual gestiona el registro de vehículos, así también las tarjetas de circulación de los mismos. Este proyecto combina un backend en Python y un frontend de escritorio moderno en PyQt6 para mantener vehículos, propietarios y estados en línea de forma intuitiva, conectándose a una base de datos PostgreSQL local.

## 🌟 Qué hace

- Administra vehículos, propietarios y tarjetas de circulación.
- Crea nuevas tarjetas con verificación de VIN y placa.
- Cambia dueño, motor o color desde el módulo de mantenimiento.
- Desactiva y reactiva tarjetas cuando se requiera.
- Guarda un historial de cambios detallado para cada operación.
- Gestión dinámica de catálogos y validaciones de seguridad paso a paso.

## 🧩 Estructura principal

- `Proyecto/backend/`: API y lógica de negocio.
- `Proyecto/frontend/`: aplicación de escritorio en PyQt6.
- `Proyecto/Docs/`: documentación, datos de ejemplo y esquema de base de datos.


## 🚀 Cómo ejecutarlo

1. Instala las dependencias del proyecto:
   ```bash
   pip install -r Proyecto/requirements.txt
   ```
2. Configura tu `.env` con la URL de tu base de datos PostgreSQL:
   - `DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/tarjetas_db`
3. Entra a la carpeta del proyecto:
   ```bash
   cd Proyecto
   ```
4. Inicia el backend (servidor FastAPI):
   ```bash
   python -m uvicorn backend.main:app --reload
   ```
5. En otra terminal, arranca el frontend (recuerda hacer `cd Proyecto` primero):
   ```bash
   python frontend/main.py
   ```

> El frontend se conecta por defecto al backend en `http://127.0.0.1:8000/api`.

## 🎯 Lo más destacado

- Diseño modular: backend separado de frontend.
- Base de datos relacional robusta (PostgreSQL).
- Doble modo de backend: FastAPI cuando esté disponible y servidor HTTP simple como respaldo.
- UX adaptada a escritorio con temas oscuros y botones de baja tensión visual.
- Registro de historial para cada cambio crítico.

## 💡 Idea rápida

Si quieres extender el sistema, puedes agregar:
- validación de usuario en el backend,
- filtros avanzados en la vista de tarjetas,
- o una pantalla de auditoría para ver sólo los cambios de estado.

## 📁 ¿Dónde empezar?

- Para backend: `Proyecto/backend/services/tarjetas_service.py`
- Para frontend: `Proyecto/frontend/views/mantenimiento_view.py`
- Para datos: `Proyecto/Docs/db_schema.sql`

