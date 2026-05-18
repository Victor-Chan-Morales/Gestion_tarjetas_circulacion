import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

try:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware

    from backend.routes.tarjetas import router as tarjetas_router

    app = FastAPI(title="SAT Guatemala API")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(tarjetas_router)

    @app.get("/")
    def root():
        return {"app": "SAT Guatemala API", "status": "ok"}

except ModuleNotFoundError:
    from backend.services import tarjetas_service

    class AppInfo:
        title = "SAT Guatemala API"

    app = AppInfo()

    class Handler(BaseHTTPRequestHandler):
        def _body(self):
            length = int(self.headers.get("Content-Length", 0))
            if not length:
                return {}
            return json.loads(self.rfile.read(length).decode("utf-8"))

        def _send(self, data, status=200):
            raw = json.dumps(data, default=str).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
            self.end_headers()
            self.wfile.write(raw)

        def do_OPTIONS(self):
            self._send({"ok": True})

        def do_GET(self):
            path = urlparse(self.path).path
            try:
                if path == "/":
                    self._send({"app": "SAT Guatemala API", "status": "ok"})
                elif path == "/api/health":
                    self._send({"ok": True})
                elif path == "/api/catalogos":
                    self._send(tarjetas_service.catalogos())
                elif path == "/api/tarjetas":
                    self._send(tarjetas_service.listar_tarjetas())
                elif path == "/api/historial":
                    self._send(tarjetas_service.listar_historial())
                else:
                    self._send({"detail": "Ruta no encontrada"}, 404)
            except Exception as exc:
                self._send({"detail": str(exc)}, 500)

        def do_POST(self):
            path = urlparse(self.path).path
            payload = self._body()
            try:
                if path == "/api/tarjetas":
                    self._send(tarjetas_service.crear_tarjeta(payload))
                elif path == "/api/mantenimiento/dueno":
                    self._send(tarjetas_service.actualizar_propietario(payload["id_tarjeta"], payload["id_propietario"], payload.get("observaciones", "")))
                elif path == "/api/mantenimiento/motor":
                    self._send(tarjetas_service.actualizar_motor(payload["vin"], payload["id_tarjeta"], payload["motor"], payload["cilindros"], payload["cc"], payload.get("observaciones", "")))
                elif path == "/api/mantenimiento/color":
                    self._send(tarjetas_service.actualizar_color(payload["vin"], payload["id_tarjeta"], payload["id_color"], payload.get("observaciones", "")))
                elif path == "/api/mantenimiento/activar":
                    self._send(tarjetas_service.activar_tarjeta(payload["id_tarjeta"], payload.get("observaciones", "")))
                elif path == "/api/desactivaciones":
                    self._send(tarjetas_service.desactivar_tarjeta(payload["id_tarjeta"], payload["motivo"], payload.get("observaciones", "")))
                else:
                    self._send({"detail": "Ruta no encontrada"}, 404)
            except Exception as exc:
                self._send({"detail": str(exc)}, 500)


def run(host="127.0.0.1", port=8000):
    if "Handler" not in globals():
        import uvicorn
        uvicorn.run("backend.main:app", host=host, port=port, reload=True)
        return
    server = HTTPServer((host, port), Handler)
    print(f"SAT Guatemala API escuchando en http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
