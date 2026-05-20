from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QListWidget, QListWidgetItem, QMessageBox
from PyQt6.QtCore import Qt

from services.api_client import desactivar_tarjeta, obtener_tarjetas
from widgets.ui_helpers import PAGE_BG, badge, card, combo, danger_button, estado_color, input_field, label, text_area


def dato(registro, *ruta, default=""):
    valor = registro
    for clave in ruta:
        if not isinstance(valor, dict):
            return default
        valor = valor.get(clave)
    return default if valor in (None, "") else str(valor)


class DesactivacionesView(QWidget):

    def __init__(self):
        super().__init__()
        self.tarjetas = []
        self.tarjeta = None
        self.init_ui()
        self.refresh_data()

    def init_ui(self):
        self.setStyleSheet(f"background:{PAGE_BG};")
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 28, 30, 30)
        layout.setSpacing(24)

        title = QVBoxLayout()
        lbl_des = label("Desactivacion de Tarjetas", bold=True)
        lbl_des.setStyleSheet("color:#E2E8F0; font-size:23px; font-weight:800; background:transparent; border:none;")
        title.addWidget(lbl_des)
        lbl_desc = label("Desactivar tarjetas por impago o vencimiento", muted=True)
        lbl_desc.setStyleSheet("color:#94A3B8; font-size:15px; background:transparent; border:none;")
        title.addWidget(lbl_desc)
        layout.addLayout(title)

        body = QHBoxLayout()
        body.setSpacing(22)
        body.addWidget(self.panel_lista())
        body.addWidget(self.panel_detalle(), 1)
        layout.addLayout(body)
        self.setLayout(layout)
        self.refrescar_detalle()

    def panel_lista(self):
        frame = card()
        frame.setFixedWidth(320)
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        layout.addWidget(label("Tarjetas Activas", bold=True))
        self.count_label = label(f"{len(self.tarjetas)} tarjetas disponibles", muted=True)
        layout.addWidget(self.count_label)
        self.buscar = input_field("Buscar tarjeta activa...")
        self.buscar.textChanged.connect(self.filtrar)
        layout.addWidget(self.buscar)
        self.lista = QListWidget()
        self.lista.setStyleSheet("""
            QListWidget{border:none; background:#0F172A; outline:none; color:#E2E8F0;}
            QListWidget::item{
                border:1px solid #1F2937;
                border-radius:10px;
                padding:10px;
                margin-bottom:8px;
                color:#E2E8F0;
                background:#0F172A;
            }
            QListWidget::item:selected{
                border:1px solid #2563EB;
                background:#1A365D;
                color:#FFFFFF;
            }
            QListWidget::item:hover{
                border:1px solid #2563EB;
                background:#11213B;
            }
        """)
        self.lista.currentRowChanged.connect(self.seleccionar_actual)
        layout.addWidget(self.lista, 1)
        frame.setLayout(layout)
        self.filtrar()
        return frame

    def refresh_data(self):
        self.tarjetas = [t for t in obtener_tarjetas() if dato(t, "estado", "nombre_estado") == "Activa"]
        self.tarjeta = self.tarjetas[0] if self.tarjetas else None
        if hasattr(self, "count_label"):
            self.count_label.setText(f"{len(self.tarjetas)} tarjetas disponibles")
        if hasattr(self, "lista"):
            self.filtrar()
        if hasattr(self, "detalle_layout"):
            self.refrescar_detalle()

    def panel_detalle(self):
        self.detalle = card()
        self.detalle_layout = QVBoxLayout()
        self.detalle_layout.setContentsMargins(22, 18, 22, 22)
        self.detalle_layout.setSpacing(18)
        self.detalle.setLayout(self.detalle_layout)
        return self.detalle

    def filtrar(self):
        texto = self.buscar.text().lower() if hasattr(self, "buscar") else ""
        self.lista.clear()
        for tarjeta in self.tarjetas:
            searchable = " ".join([
                dato(tarjeta, "codigo_identificador"),
                dato(tarjeta, "vehiculo", "placa"),
                dato(tarjeta, "propietario", "nombre"),
            ]).lower()
            if texto and texto not in searchable:
                continue
            item = QListWidgetItem(
                f"{dato(tarjeta, 'codigo_identificador')}        Vence: {dato(tarjeta, 'vigencia')}\n"
                f"{dato(tarjeta, 'vehiculo', 'placa')}\n"
                f"{dato(tarjeta, 'propietario', 'nombre')}"
            )
            item.setData(Qt.ItemDataRole.UserRole, tarjeta)
            self.lista.addItem(item)
        if self.lista.count():
            self.lista.setCurrentRow(0)

    def seleccionar_actual(self):
        item = self.lista.currentItem()
        if item:
            self.tarjeta = item.data(Qt.ItemDataRole.UserRole)
            if hasattr(self, "detalle_layout"):
                self.refrescar_detalle()

    def refrescar_detalle(self):
        from widgets.ui_helpers import clear_layout

        clear_layout(self.detalle_layout)
        if not self.tarjeta:
            self.detalle_layout.addWidget(label("No hay tarjetas activas", muted=True))
            return

        header = QHBoxLayout()
        texts = QVBoxLayout()
        texts.addWidget(label("Desactivar Tarjeta", bold=True))
        texts.addWidget(label(dato(self.tarjeta, "codigo_identificador"), muted=True))
        header.addLayout(texts)
        header.addStretch()
        header.addWidget(badge(dato(self.tarjeta, "estado", "nombre_estado"), estado_color(dato(self.tarjeta, "estado", "nombre_estado"))))
        self.detalle_layout.addLayout(header)

        info = card()
        grid = QGridLayout()
        grid.setContentsMargins(16, 14, 16, 14)
        marca = dato(self.tarjeta, "vehiculo", "linea", "marca", "nombre_marca")
        linea = dato(self.tarjeta, "vehiculo", "linea", "nombre_linea")
        grid.addWidget(label("Informacion de la Tarjeta", bold=True), 0, 0, 1, 4)
        valores = [
            ("Placa:", dato(self.tarjeta, "vehiculo", "placa")),
            ("VIN:", dato(self.tarjeta, "vehiculo", "vin")),
            ("Vehiculo:", f"{marca} {linea}"),
            ("Modelo:", dato(self.tarjeta, "vehiculo", "modelo")),
            ("Propietario:", dato(self.tarjeta, "propietario", "nombre")),
            ("Vigencia:", dato(self.tarjeta, "vigencia")),
        ]
        for idx, (key, val) in enumerate(valores, start=1):
            col = 0 if idx % 2 else 2
            row = (idx + 1) // 2
            grid.addWidget(label(key, muted=True), row, col)
            grid.addWidget(label(val), row, col + 1)
        info.setLayout(grid)
        self.detalle_layout.addWidget(info)

        self.motivo = combo(["Seleccionar motivo", "Impago", "Vencimiento", "Solicitud del propietario", "Error administrativo"])
        self.obs = text_area("Detalles adicionales sobre la desactivacion...")
        self.detalle_layout.addWidget(label("Motivo de Desactivacion"))
        self.detalle_layout.addWidget(self.motivo)
        self.detalle_layout.addWidget(label("Observaciones Adicionales"))
        self.detalle_layout.addWidget(self.obs)

        actions = QHBoxLayout()
        actions.addStretch()
        btn = danger_button("Desactivar Tarjeta")
        btn.clicked.connect(self.desactivar)
        actions.addWidget(btn)
        self.detalle_layout.addLayout(actions)

        
        self.detalle_layout.addStretch()


    def desactivar(self):
        try:
            if not self.tarjeta:
                raise ValueError("Seleccione una tarjeta activa.")
            if self.motivo.currentIndex() == 0:
                raise ValueError("Seleccione un motivo de desactivacion.")
                
            confirm = QMessageBox.question(
                self, "Confirmar", 
                "¿Esta seguro que desea desactivar esta tarjeta de forma definitiva?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if confirm != QMessageBox.StandardButton.Yes:
                return
                
            desactivar_tarjeta({
                "id_tarjeta": self.tarjeta["id_tarjeta"],
                "motivo": self.motivo.currentText(),
                "observaciones": self.obs.toPlainText(),
            })
            QMessageBox.information(self, "Tarjeta desactivada", "La tarjeta fue desactivada correctamente.")
            self.refresh_data()
        except Exception as exc:
            QMessageBox.warning(self, "Error", str(exc))
