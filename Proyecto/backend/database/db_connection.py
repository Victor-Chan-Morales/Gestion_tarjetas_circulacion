import os
import psycopg2
from psycopg2.extras import RealDictCursor
from backend.database.env import load_env

load_env()

# Asumimos que la URL de base de datos se proporcionará en .env
DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    """
    Crea y devuelve una conexión a la base de datos PostgreSQL.
    """
    if not DATABASE_URL:
        raise RuntimeError("Falta DATABASE_URL en el archivo .env")
    
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    return conn

def execute_query(query, params=None, fetch=True):
    """
    Ejecuta una consulta SQL. 
    Si fetch es True, devuelve los resultados como una lista de diccionarios.
    """
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            if fetch:
                return cur.fetchall()
            return None
    finally:
        conn.close()

def execute_modify(query, params=None, returning=False):
    """
    Ejecuta un INSERT, UPDATE o DELETE.
    Si returning es True, devuelve la fila afectada.
    """
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            if returning:
                return cur.fetchone()
            return None
    finally:
        conn.close()
