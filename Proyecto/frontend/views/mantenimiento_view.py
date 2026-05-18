from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QListWidget, QListWidgetItem, QMessageBox
from PyQt6.QtCore import Qt

from services.api_client import (
    obtener_catalogos,
    obtener_tarjetas,
    registrar_cambio_color,
    registrar_cambio_dueno,
    registrar_cambio_motor,
    reactivar_tarjeta,
)
from widgets.ui_helpers import (
    BLUE,
    PAGE_BG,
    badge,
    card,
    combo,
    estado_color,
    input_field,
    label,
    primary_button,
    text_area,
)


def dato(registro, *ruta, default=""):
    valor = registro
    for clave in ruta:
        if not isinstance(valor, dict):
            return default
        valor = valor.get(clave)
    return default if valor in (None, "") else str(valor)


class MantenimientoView(QWidget):

    def __init__(self):
        super().__init__()
        self.tarjetas = []
        self.catalogos = obtener_catalogos()
        self.tarjeta = None
        self.modo = "dueno"
        self.init_ui()
        self.refresh_data()

    def init_ui(self):
        self.setStyleSheet(f"background:{PAGE_BG};")
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 28, 30, 30)
        layout.setSpacing(24)

        title = QVBoxLayout()
        
        lbl_man = label("Mantenimiento de tarjetas", bold=True)
        lbl_man.setStyleSheet("color:#E2E8F0; font-size:23px; font-weight:800; background:transparent; border:none;")
        title.addWidget(lbl_man)
        
        lbl_camb = label("Cambio de dueno, motor o color de vehiculos", muted=True)
        lbl_camb.setStyleSheet("color:#94A3B8; font-size:15px; background:transparent; border:none;")
        title.addWidget(lbl_camb)
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

        layout.addWidget(label("Seleccionar Tarjeta", bold=True))
        layout.addWidget(label("Busque por codigo, placa o propietario", muted=True))

        self.buscar = input_field("Buscar tarjeta...")
        self.buscar.textChanged.connect(self.filtrar)
        layout.addWidget(self.buscar)

        self.lista = QListWidget()
        self.lista.setStyleSheet("""
            QListWidget{
                border:none;
                background:#0F172A;
                outline:none;
                color:#E2E8F0;
            }
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
                background:#102134;
            }
        """)
        self.lista.currentRowChanged.connect(self.seleccionar_actual)
        layout.addWidget(self.lista, 1)

        frame.setLayout(layout)
        self.filtrar()
        return frame

    def refresh_data(self):
        self.tarjetas = obtener_tarjetas()
        self.catalogos = obtener_catalogos()
        self.tarjeta = self.tarjetas[0] if self.tarjetas else None
        if hasattr(self, "lista"):
            self.filtrar()
        if hasattr(self, "detalle_layout"):
            self.refrescar_detalle()

    def panel_detalle(self):
        self.detalle = card()
        self.detalle.setMinimumWidth(610)
        self.detalle_layout = QVBoxLayout()
        self.detalle_layout.setContentsMargins(22, 18, 22, 22)
        self.detalle_layout.setSpacing(14) 
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
                f"{dato(tarjeta, 'codigo_identificador')}\n"
                f"{dato(tarjeta, 'vehiculo', 'placa')}\n"
                f"{dato(tarjeta, 'propietario', 'nombre')}"
            )
            item.setData(Qt.ItemDataRole.UserRole, tarjeta)
            item.setSizeHint(item.sizeHint())
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
        from widgets.ui_helpers import clear_layout, secondary_button

        clear_layout(self.detalle_layout)
        if not self.tarjeta:
            self.detalle_layout.addWidget(label("No hay tarjetas disponibles", muted=True))
            return

        marca = dato(self.tarjeta, "vehiculo", "linea", "marca", "nombre_marca")
        linea = dato(self.tarjeta, "vehiculo", "linea", "nombre_linea")
        header = QHBoxLayout()
        header_text = QVBoxLayout()
        header_text.addWidget(label(f"{dato(self.tarjeta, 'vehiculo', 'placa')} - {marca} {linea}", bold=True))
        header_text.addWidget(label(f"Propietario: {dato(self.tarjeta, 'propietario', 'nombre')}", muted=True))
        header.addLayout(header_text)
        header.addStretch()
        if dato(self.tarjeta, "estado", "nombre_estado") != "Activa":
            activar_btn = primary_button("Reactivar tarjeta")
            activar_btn.clicked.connect(self.reactivar_tarjeta)
            header.addWidget(activar_btn)
        header.addWidget(badge(dato(self.tarjeta, "estado", "nombre_estado"), estado_color(dato(self.tarjeta, "estado", "nombre_estado"))))
        self.detalle_layout.addLayout(header)

        tabs = QHBoxLayout()
        for key, text in [("dueno", "Cambio de Dueno"), ("motor", "Cambio de Motor"), ("color", "Cambio de Color")]:
            btn = secondary_button(text)
            if key == self.modo:
                btn.setStyleSheet(f"background:#111827; border:2px solid #2563EB; border-radius:8px; font-weight:700;")
            btn.clicked.connect(lambda checked=False, k=key: self.cambiar_modo(k))
            tabs.addWidget(btn)
        tabs.addStretch()
        self.detalle_layout.addLayout(tabs)

        if self.modo == "dueno":
            self.form_dueno()
        elif self.modo == "motor":
            self.form_motor()
        else:
            self.form_color()

    def cambiar_modo(self, modo):
        self.modo = modo
        self.refrescar_detalle()

    def form_dueno(self):
        grid = QGridLayout()
        grid.setVerticalSpacing(8)
        grid.addWidget(label("Propietario Actual", bold=True), 0, 0, 1, 2)
        for row, key in enumerate(["nombre", "nit", "cui"], start=1):
            grid.addWidget(label(key.upper() + ":", muted=True), row, 0)
            grid.addWidget(label(dato(self.tarjeta, "propietario", key)), row, 1)
        self.detalle_layout.addLayout(grid)

        self.propietario_nuevo = combo(["Seleccionar propietario existente"])
        for prop in self.catalogos["propietarios"]:
            self.propietario_nuevo.addItem(prop["nombre"], prop["id_propietario"])
        
        self.obs_dueno = text_area("Motivo del cambio de propietario...")
        self.obs_dueno.setMaximumHeight(100) 
        
        self.detalle_layout.addWidget(label("Seleccionar Propietario", bold=True))
        self.detalle_layout.addWidget(self.propietario_nuevo)
        self.detalle_layout.addWidget(label("Observaciones", bold=True))
        self.detalle_layout.addWidget(self.obs_dueno)
        self._action("Registrar Cambio de Dueno", self.guardar_dueno)
        
        self.detalle_layout.addStretch()

    def form_motor(self):
        grid = QGridLayout()
        grid.setVerticalSpacing(8)
        grid.addWidget(label("Motor Actual", bold=True), 0, 0, 1, 2)
        grid.addWidget(label("Numero de Motor:", muted=True), 1, 0)
        grid.addWidget(label(dato(self.tarjeta, "vehiculo", "motor")), 1, 1)
        grid.addWidget(label("Cilindros:", muted=True), 2, 0)
        grid.addWidget(label(dato(self.tarjeta, "vehiculo", "cilindros")), 2, 1)
        grid.addWidget(label("Cilindrada:", muted=True), 3, 0)
        grid.addWidget(label(f"{dato(self.tarjeta, 'vehiculo', 'cc')} cc"), 3, 1)
        self.detalle_layout.addLayout(grid)

        self.motor_nuevo = input_field("Ej: MOT-NEW-001")
        self.cil_nuevo = input_field("Ej: 4")
        self.cc_nuevo = input_field("Ej: 2000")
        
        self.obs_motor = text_area("Motivo del cambio de motor...")
        self.obs_motor.setMaximumHeight(100)
        
        self.detalle_layout.addWidget(label("Datos del Nuevo Motor", bold=True))
        self.detalle_layout.addWidget(label("Numero de Motor"))
        self.detalle_layout.addWidget(self.motor_nuevo)
        
        row_inputs = QHBoxLayout()
        row_inputs.setSpacing(12)
        
        vbox_cil = QVBoxLayout()
        vbox_cil.addWidget(label("Cilindros"))
        vbox_cil.addWidget(self.cil_nuevo)
        
        vbox_cc = QVBoxLayout()
        vbox_cc.addWidget(label("Cilindrada (CC)"))
        vbox_cc.addWidget(self.cc_nuevo)
        
        row_inputs.addLayout(vbox_cil)
        row_inputs.addLayout(vbox_cc)
        self.detalle_layout.addLayout(row_inputs)
        
        self.detalle_layout.addWidget(label("Observaciones", bold=True))
        self.detalle_layout.addWidget(self.obs_motor)
        self._action("Registrar Cambio de Motor", self.guardar_motor)
        
        self.detalle_layout.addStretch()

    def form_color(self):
        self.color_nuevo = combo(["Seleccionar nuevo color"])
        for color in self.catalogos["colores"]:
            self.color_nuevo.addItem(color["nombre_color"], color["id_color"])
            
        self.obs_color = text_area("Motivo del cambio de color...")
        self.obs_color.setMaximumHeight(100) # Controlamos altura máxima del campo
        
        self.detalle_layout.addWidget(label(f"Color Actual:  {dato(self.tarjeta, 'vehiculo', 'color', 'nombre_color')}", bold=True))
        self.detalle_layout.addWidget(label("Nuevo Color", bold=True))
        self.detalle_layout.addWidget(self.color_nuevo)
        self.detalle_layout.addWidget(label("Observaciones", bold=True))
        self.detalle_layout.addWidget(self.obs_color)
        self._action("Registrar Cambio de Color", self.guardar_color)
        
       
        self.detalle_layout.addStretch()

    def _action(self, text, handler):
        row = QHBoxLayout()
        row.addStretch()
        btn = primary_button(text)
        btn.clicked.connect(handler)
        row.addWidget(btn)
        self.detalle_layout.addLayout(row)

    def guardar_dueno(self):
        try:
            if not self.propietario_nuevo.currentData():
                raise ValueError("Seleccione el nuevo propietario.")
            registrar_cambio_dueno({
                "id_tarjeta": self.tarjeta["id_tarjeta"],
                "id_propietario": self.propietario_nuevo.currentData(),
                "observaciones": self.obs_dueno.toPlainText(),
            })
            QMessageBox.information(self, "Cambio registrado", "Cambio de dueno registrado correctamente.")
            self.refresh_data()
        except Exception as exc:
            QMessageBox.warning(self, "Error", str(exc))

    def guardar_motor(self):
        try:
            if not self.motor_nuevo.text().strip():
                raise ValueError("Ingrese el numero del nuevo motor.")
            registrar_cambio_motor({
                "id_tarjeta": self.tarjeta["id_tarjeta"],
                "vin": dato(self.tarjeta, "vehiculo", "vin"),
                "motor": self.motor_nuevo.text(),
                "cilindros": int(self.cil_nuevo.text()),
                "cc": int(self.cc_nuevo.text()),
                "observaciones": self.obs_motor.toPlainText(),
            })
            QMessageBox.information(self, "Cambio registrado", "Cambio de motor registrado correctamente.")
            self.refresh_data()
        except Exception as exc:
            QMessageBox.warning(self, "Error", str(exc))
    def reactivar_tarjeta(self):
        try:
            if dato(self.tarjeta, "estado", "nombre_estado") == "Activa":
                raise ValueError("La tarjeta ya se encuentra activa.")
            reactivar_tarjeta({
                "id_tarjeta": self.tarjeta["id_tarjeta"],
                "observaciones": "Reactivacion desde mantenimiento",
            })
            QMessageBox.information(self, "Tarjeta reactivada", "La tarjeta se ha reactivado correctamente.")
            self.refresh_data()
        except Exception as exc:
            QMessageBox.warning(self, "Error", str(exc))
    def guardar_color(self):
        try:
            if not self.color_nuevo.currentData():
                raise ValueError("Seleccione el nuevo color.")
            registrar_cambio_color({
                "id_tarjeta": self.tarjeta["id_tarjeta"],
                "vin": dato(self.tarjeta, "vehiculo", "vin"),
                "id_color": self.color_nuevo.currentData(),
                "observaciones": self.obs_color.toPlainText(),
            })
            QMessageBox.information(self, "Cambio registrado", "Cambio de color registrado correctamente.")
            self.refresh_data()
        except Exception as exc:
            QMessageBox.warning(self, "Error", str(exc))