import json
import os
import urllib.parse
import urllib.request

from .env import load_env


load_env()

SUPABASE_URL = os.getenv("SUPABASE_URL", "").rstrip("/")
SUPABASE_KEY = (
    os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    or os.getenv("SUPABASE_SERVICE_KEY")
    or os.getenv("SERVICE_ROLE_KEY")
    or os.getenv("SUPABASE_KEY")
    or os.getenv("SUPABASE_ANON_KEY")
    or ""
)


class SupabaseError(RuntimeError):
    pass


def _headers(prefer=None):
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise SupabaseError("Faltan SUPABASE_URL y SUPABASE_SERVICE_ROLE_KEY/SUPABASE_KEY en .env")

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    if prefer:
        headers["Prefer"] = prefer
    return headers


def request(table, method="GET", select=None, filters=None, payload=None, prefer="return=representation"):
    query = {}
    if select:
        query["select"] = select
    if filters:
        query.update(filters)

    qs = urllib.parse.urlencode(query, safe="(),.:*")
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    if qs:
        url = f"{url}?{qs}"

    body = None
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=body,
        method=method,
        headers=_headers(prefer if method in ("POST", "PATCH", "DELETE") else None),
    )

    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw) if raw else []
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8")
        try:
            parsed = json.loads(detail)
            message = parsed.get("message") or parsed.get("detail") or detail
            hint = parsed.get("hint")
            if hint:
                message = f"{message}. Hint: {hint}"
        except Exception:
            message = detail
        if "permission denied for schema public" in message.lower():
            message = (
                "Supabase nego permisos sobre el schema public. "
                "Ejecuta los GRANT del proyecto en Supabase SQL Editor para service_role."
            )
        raise SupabaseError(message) from exc


def first(table, select="*", filters=None):
    data = request(table, select=select, filters=filters or {})
    return data[0] if data else None
