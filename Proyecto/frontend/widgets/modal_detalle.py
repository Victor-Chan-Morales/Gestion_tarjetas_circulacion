from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QGridLayout,
)

from PyQt6.QtCore import Qt


def dato(registro, *ruta, default=""):
    valor = registro
    for clave in ruta:
        if not isinstance(valor, dict):
            return default
        valor = valor.get(clave)
    return default if valor in (None, "") else str(valor)


class ModalDetalleTarjeta(QDialog):
    def __init__(self, tarjeta, parent=None):
        super().__init__(parent)
        self.tarjeta = tarjeta
        self.setWindowTitle("Detalle de Tarjeta")
        self.setModal(True)
        self.setFixedWidth(520)
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QDialog{
                background:#0B1220;
                border-radius:14px;
            }
            QLabel{
                color:#E2E8F0;
                font-size:14px;
            }
            QPushButton{
                border-radius:9px;
                padding:9px 16px;
                font-weight:600;
                font-size:14px;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(16)

        header = QHBoxLayout()
        titulo = QLabel("Detalle de Tarjeta de Circulacion")
        titulo.setStyleSheet("font-size:18px; font-weight:700; color:#E2E8F0;")

        cerrar = QPushButton("x")
        cerrar.setFixedSize(28, 28)
        cerrar.setCursor(Qt.CursorShape.PointingHandCursor)
        cerrar.setStyleSheet("""
            QPushButton{
                background:transparent;
                border:none;
                color:#94A3B8;
                font-size:18px;
                padding:0;
            }
            QPushButton:hover{background:#112134;}
        """)
        cerrar.clicked.connect(self.close)

        header.addWidget(titulo)
        header.addStretch()
        header.addWidget(cerrar)

        codigo = QLabel(f"Codigo: {dato(self.tarjeta, 'codigo_identificador')}")
        codigo.setStyleSheet("color:#94A3B8;")

        contenido = QHBoxLayout()
        contenido.setSpacing(16)
        contenido.addWidget(self.card_vehiculo())
        contenido.addWidget(self.card_propietario())

        layout.addLayout(header)
        layout.addWidget(codigo)
        layout.addLayout(contenido)

        self.setLayout(layout)

    def card_vehiculo(self):
        vehiculo = dato(self.tarjeta, "vehiculo", default={})
        frame = self._card("Informacion del\nVehiculo")
        grid = frame.layout()

        marca = dato(self.tarjeta, "vehiculo", "linea", "marca", "nombre_marca")
        linea = dato(self.tarjeta, "vehiculo", "linea", "nombre_linea")
        cilindros = dato(self.tarjeta, "vehiculo", "cilindros")
        cc = dato(self.tarjeta, "vehiculo", "cc")

        filas = [
            ("VIN:", dato(self.tarjeta, "vehiculo", "vin")),
            ("Placa:", dato(self.tarjeta, "vehiculo", "placa")),
            ("Marca/Linea:", f"{marca} {linea}".strip()),
            ("Modelo:", dato(self.tarjeta, "vehiculo", "modelo")),
            ("Tipo:", dato(self.tarjeta, "vehiculo", "tipo_vehiculo", "nombre_tipo")),
            ("Color:", dato(self.tarjeta, "vehiculo", "color", "nombre_color")),
            ("Motor:", dato(self.tarjeta, "vehiculo", "motor")),
            ("Cilindros/CC:", f"{cilindros} cil / {cc} cc"),
        ]

        self._agregar_filas(grid, filas)
        return frame

    def card_propietario(self):
        frame = self._card("Informacion del\nPropietario")
        grid = frame.layout()

        filas = [
            ("Nombre:", dato(self.tarjeta, "propietario", "nombre")),
            ("NIT:", dato(self.tarjeta, "propietario", "nit")),
            ("CUI:", dato(self.tarjeta, "propietario", "cui")),
            ("", ""),
            ("Estado:", dato(self.tarjeta, "estado", "nombre_estado")),
            ("Uso:", dato(self.tarjeta, "uso", "nombre_uso")),
            ("Registro:", dato(self.tarjeta, "fecha_registro")),
            ("Emision:", f"{dato(self.tarjeta, 'fecha_emision')} - {dato(self.tarjeta, 'hora_emision')}"),
            ("Vigencia:", dato(self.tarjeta, "vigencia")),
        ]

        self._agregar_filas(grid, filas, estado=True)
        return frame

    def _card(self, titulo):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame{
                background:#111827;
                border:1px solid #1F2937;
                border-radius:10px;
            }
        """)
        frame.setMinimumWidth(210)

        layout = QGridLayout()
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setHorizontalSpacing(8)
        layout.setVerticalSpacing(10)

        label = QLabel(titulo)
        label.setStyleSheet("font-size:16px; font-weight:700; color:#E2E8F0; border:none;")
        layout.addWidget(label, 0, 0, 1, 2)

        frame.setLayout(layout)
        return frame

    def _agregar_filas(self, grid, filas, estado=False):
        fila_grid = 1
        for etiqueta, valor in filas:
            if not etiqueta:
                espacio = QLabel("Estado de la Tarjeta")
                espacio.setStyleSheet("font-size:16px; font-weight:700; color:#E2E8F0; border:none; margin-top:10px;")
                grid.addWidget(espacio, fila_grid, 0, 1, 2)
                fila_grid += 1
                continue

            key = QLabel(etiqueta)
            key.setStyleSheet("color:#94A3B8; border:none;")

            value = QLabel(valor)
            value.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            value.setWordWrap(True)
            value.setStyleSheet("color:#E2E8F0; border:none;")

            if estado and etiqueta == "Estado:":
                value.setText(valor)
                value.setAlignment(Qt.AlignmentFlag.AlignCenter)
                value.setStyleSheet(f"""
                    color:white;
                    background:{color_estado(valor)};
                    border:none;
                    border-radius:9px;
                    padding:3px 9px;
                    font-weight:700;
                """)

            grid.addWidget(key, fila_grid, 0)
            grid.addWidget(value, fila_grid, 1)
            fila_grid += 1


def color_estado(estado):
    estado = (estado or "").strip().lower()
    if estado == "activa":
        return "#2E7D45"
    if "vencida" in estado:
        return "#D90429"
    if "suspendida" in estado:
        return "#D99A00"
    return "#94A3B8"
