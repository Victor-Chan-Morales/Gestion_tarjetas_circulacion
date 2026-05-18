from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout

from services.api_client import obtener_historial, obtener_tarjetas
from widgets.ui_helpers import PAGE_BG, card, clear_layout, label


def dato(registro, *ruta, default=""):
    valor = registro
    for clave in ruta:
        if not isinstance(valor, dict):
            return default
        valor = valor.get(clave)
    return default if valor in (None, "") else str(valor)


class DashboardHomeView(QWidget):
    def __init__(self):
        super().__init__()
        self.tarjetas = []
        self.historial = []
        self.setStyleSheet(f"background:{PAGE_BG};")
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(30, 28, 30, 30)
        self.layout.setSpacing(22)
        self.setLayout(self.layout)
        self.refresh_data()

    def refresh_data(self):
        self.tarjetas = obtener_tarjetas()
        self.historial = obtener_historial()
        self.render()

    def render(self):
        clear_layout(self.layout)
        title = QVBoxLayout()
        lbl_dash = label("Dashboard", bold=True)
        lbl_dash.setStyleSheet("color:#E2E8F0; font-size:23px; font-weight:800; background:transparent; border:none;")
        title.addWidget(lbl_dash)
        
        lbl_res = label("Resumen general de tarjetas de circulacion", muted=True)
        lbl_res.setStyleSheet("color:#94A3B8; font-size:15px; background:transparent; border:none;")
        title.addWidget(lbl_res)
        self.layout.addLayout(title)

        stats = QHBoxLayout()
        total = len(self.tarjetas)
        activas = sum(1 for t in self.tarjetas if dato(t, "estado", "nombre_estado") == "Activa")
        inactivas = sum(1 for t in self.tarjetas if dato(t, "estado", "nombre_estado") != "Activa")
        cambios = len(self.historial)
        for title_text, value in [
            ("Tarjetas Registradas", total),
            ("Tarjetas Activas", activas),
            ("No Activas", inactivas),
            ("Cambios en Historial", cambios),
        ]:
            box = card()
            box_layout = QVBoxLayout()
            box_layout.setContentsMargins(18, 16, 18, 16)
            value_label = label(str(value), bold=True)
            value_label.setStyleSheet("font-size:24px; font-weight:800; color:#E2E8F0; border:none; background:transparent;")
            box_layout.addWidget(value_label)
            box_layout.addWidget(label(title_text, muted=True))
            box.setLayout(box_layout)
            stats.addWidget(box)
        self.layout.addLayout(stats)

        latest = card()
        grid = QGridLayout()
        grid.setContentsMargins(18, 16, 18, 16)
        grid.setHorizontalSpacing(22)
        grid.addWidget(label("Ultimas Tarjetas", bold=True), 0, 0, 1, 4)
        for row, tarjeta in enumerate(self.tarjetas[:6], start=1):
            marca = dato(tarjeta, "vehiculo", "linea", "marca", "nombre_marca")
            linea = dato(tarjeta, "vehiculo", "linea", "nombre_linea")
            grid.addWidget(label(dato(tarjeta, "codigo_identificador")), row, 0)
            grid.addWidget(label(dato(tarjeta, "vehiculo", "placa")), row, 1)
            grid.addWidget(label(f"{marca} {linea}".strip()), row, 2)
            grid.addWidget(label(dato(tarjeta, "estado", "nombre_estado"), muted=True), row, 3)
        if not self.tarjetas:
            grid.addWidget(label("No hay tarjetas registradas todavia.", muted=True), 1, 0, 1, 4)
        latest.setLayout(grid)
        self.layout.addWidget(latest)
        self.layout.addStretch()
