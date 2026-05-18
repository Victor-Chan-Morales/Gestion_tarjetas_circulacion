from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt

from services.api_client import obtener_historial, obtener_catalogos
from widgets.ui_helpers import PAGE_BG, card, combo, input_field, label


def dato(registro, *ruta, default=""):
    valor = registro
    for clave in ruta:
        if not isinstance(valor, dict):
            return default
        valor = valor.get(clave)
    return default if valor in (None, "") else str(valor)


class HistorialView(QWidget):
    def __init__(self):
        super().__init__()
        self.historial = []
        self.filtrado = []
        self.catalogos = {}
        self.stat_labels = {}
        self.init_ui()
        self.refresh_data()

    def init_ui(self):
        self.setStyleSheet(f"background:{PAGE_BG};")
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 28, 30, 30)
        layout.setSpacing(22)

        title = QVBoxLayout()
        lbl_hist = label("Historial de Cambios", bold=True)
        lbl_hist.setStyleSheet("color:#E2E8F0; font-size:23px; font-weight:800; background:transparent; border:none;")
        title.addWidget(lbl_hist)
        lbl_desc = label("Registro de todos los cambios realizados a las tarjetas", muted=True)
        lbl_desc.setStyleSheet("color:#94A3B8; font-size:15px; background:transparent; border:none;")
        title.addWidget(lbl_desc)
        layout.addLayout(title)

        stats = QHBoxLayout()
        for tipo, icon in [("CAMBIO DUENO", ""), ("CAMBIO MOTOR", ""), ("CAMBIO COLOR", "")]:
            box = card()
            box_layout = QHBoxLayout()
            box_layout.setContentsMargins(16, 14, 16, 14)
            box_layout.addWidget(label(icon, bold=True))
            stat = label("0", bold=True)
            self.stat_labels[tipo] = stat
            box_layout.addWidget(stat)
            box_layout.addWidget(label(tipo.title(), muted=True))
            box_layout.addStretch()
            box.setLayout(box_layout)
            stats.addWidget(box)
        layout.addLayout(stats)

        table_card = card()
        table_layout = QVBoxLayout()
        table_layout.setContentsMargins(16, 16, 16, 16)

        filtros = QHBoxLayout()
        self.buscar = input_field("Buscar por codigo, placa o valores...")
        self.tipo = combo(["Todos los tipos", "CAMBIO DUENO", "CAMBIO MOTOR", "CAMBIO COLOR", "DESACTIVACION"])
        self.buscar.textChanged.connect(self.aplicar_filtros)
        self.tipo.currentTextChanged.connect(self.aplicar_filtros)
        filtros.addWidget(self.buscar, 1)
        filtros.addWidget(self.tipo)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["Fecha", "Tarjeta", "Placa", "Tipo de Cambio", "Valor Anterior", "Valor Nuevo", "Usuario", "Observaciones"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setStyleSheet("""
            QTableWidget{background:#0F172A; border:none; font-size:13px; color:#E2E8F0;}
            QTableWidget::item{border-bottom:1px solid #1F2937; padding:7px;}
            QHeaderView::section{
                background:#0F172A;
                border:none;
                border-bottom:1px solid #1F2937;
                padding:10px 7px;
                font-weight:700;
                color:#A5B4FC;
            }
        """)

        table_layout.addLayout(filtros)
        table_layout.addWidget(self.table)
        table_card.setLayout(table_layout)
        layout.addWidget(table_card, 1)
        self.setLayout(layout)

    def refresh_data(self):
        self.historial = obtener_historial()
        self.catalogos = obtener_catalogos()
        for tipo, stat in self.stat_labels.items():
            stat.setText(str(sum(1 for h in self.historial if h.get("tipo_cambio") == tipo)))
        self.aplicar_filtros()

    def aplicar_filtros(self):
        texto = self.buscar.text().lower()
        tipo = self.tipo.currentText()
        rows = []
        for h in self.historial:
            searchable = " ".join([
                dato(h, "tarjeta", "codigo_identificador"),
                dato(h, "tarjeta", "vehiculo", "placa"),
                h.get("valor_anterior", ""),
                h.get("valor_actual", ""),
                h.get("observaciones", ""),
            ]).lower()
            if texto and texto not in searchable:
                continue
            if tipo != "Todos los tipos" and h.get("tipo_cambio") != tipo:
                continue
            rows.append(h)
        self.filtrado = rows
        self.pintar()

    def map_valor(self, tipo_cambio, valor):
        if not valor:
            return valor
        if tipo_cambio == "CAMBIO DUENO":
            for p in self.catalogos.get("propietarios", []):
                if str(p["id_propietario"]) == str(valor):
                    return p["nombre"]
        elif tipo_cambio == "CAMBIO COLOR":
            for c in self.catalogos.get("colores", []):
                if str(c["id_color"]) == str(valor):
                    return c["nombre_color"]
        return valor

    def pintar(self):
        self.table.setRowCount(len(self.filtrado))
        for row, h in enumerate(self.filtrado):
            tipo = h.get("tipo_cambio", "")
            valores = [
                h.get("fecha_cambio", "")[:10],
                dato(h, "tarjeta", "codigo_identificador"),
                dato(h, "tarjeta", "vehiculo", "placa"),
                tipo,
                self.map_valor(tipo, h.get("valor_anterior")),
                self.map_valor(tipo, h.get("valor_actual")),
                "Admin Sistema",
                h.get("observaciones", ""),
            ]
            for col, value in enumerate(valores):
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row, col, item)
