from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QFrame,
    QLineEdit,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
    QMessageBox,
)

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from services.api_client import obtener_tarjetas, eliminar_tarjeta
from widgets.modal_detalle import ModalDetalleTarjeta


def dato(registro, *ruta, default=""):
    valor = registro
    for clave in ruta:
        if not isinstance(valor, dict):
            return default
        valor = valor.get(clave)
    return default if valor in (None, "") else str(valor)


class TarjetasView(QWidget):

    def __init__(self, stack=None, navigate=None):
        super().__init__()
        self.stack = stack
        self.navigate = navigate
        self.tarjetas = []
        self.tarjetas_filtradas = []
        self.init_ui()
        self.cargar_tarjetas()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 26, 30, 30)
        main_layout.setSpacing(22)

        self.setStyleSheet("background-color:#08111F;")

        encabezado = QHBoxLayout()
        titulos = QVBoxLayout()

        titulo = QLabel("Tarjetas de Circulacion")
        titulo.setStyleSheet("color:#E2E8F0; font-size:23px; font-weight:800;")
        descripcion = QLabel("Consulta y gestion de todas las tarjetas registradas")
        descripcion.setStyleSheet("color:#94A3B8; font-size:15px;")

        titulos.addWidget(titulo)
        titulos.addWidget(descripcion)

        self.btn_nueva = QPushButton("+  Nueva Tarjeta")
        self.btn_nueva.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_nueva.setFixedHeight(34)
        self.btn_nueva.setStyleSheet("""
            QPushButton{
                background-color:#2563EB;
                color:#E2E8F0;
                border:none;
                padding:0 14px;
                border-radius:8px;
                font-weight:700;
            }
            QPushButton:hover{background-color:#1D4ED8;}
        """)
        self.btn_nueva.clicked.connect(self.abrir_nueva_tarjeta)

        encabezado.addLayout(titulos)
        encabezado.addStretch()
        encabezado.addWidget(self.btn_nueva)

        card = QFrame()
        card.setStyleSheet("""
            QFrame{
                background:#0F172A;
                border-radius:14px;
                border:1px solid #1F2937;
            }
        """)

        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(22, 22, 22, 22)
        card_layout.setSpacing(14)

        filtros_layout = QHBoxLayout()
        filtros_layout.setSpacing(10)

        self.input_busqueda = QLineEdit()
        self.input_busqueda.setPlaceholderText("Buscar por codigo, propietario, placa o VIN...")
        self.input_busqueda.setFixedHeight(36)
        self.input_busqueda.setStyleSheet("""
            QLineEdit{
                border:1px solid #1F2937;
                border-radius:9px;
                padding-left:14px;
                font-size:13px;
                background:#0E1726;
                color:#E2E8F0;
            }
            QLineEdit:focus{border-color:#2563EB;}
        """)
        self.input_busqueda.textChanged.connect(self.aplicar_filtros)

        self.combo_estado = QComboBox()
        self.combo_estado.setFixedHeight(36)
        self.combo_estado.currentTextChanged.connect(self.aplicar_filtros)

        self.combo_uso = QComboBox()
        self.combo_uso.setFixedHeight(36)
        self.combo_uso.currentTextChanged.connect(self.aplicar_filtros)

        combo_style = """
            QComboBox{
                border:1px solid #1F2937;
                border-radius:9px;
                padding:7px 12px;
                background:#0E1726;
                min-width:135px;
                color:#E2E8F0;
            }
            QComboBox:hover{border:1px solid #2563EB;}
            QComboBox::drop-down{border:none; width:24px;}
            QComboBox QAbstractItemView{
                background:#0F172A;
                color:#E2E8F0;
                selection-background-color:#17324B;
                selection-color:#E2E8F0;
                border:1px solid #1F2937;
            }
        """
        self.combo_estado.setStyleSheet(combo_style)
        self.combo_uso.setStyleSheet(combo_style)

        filtros_layout.addWidget(self.input_busqueda, 1)
        filtros_layout.addWidget(self.combo_estado)
        filtros_layout.addWidget(self.combo_uso)

        self.total = QLabel("Mostrando 0 de 0 tarjetas")
        self.total.setStyleSheet("color:#94A3B8; font-size:13px;")

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Codigo",
            "Propietario",
            "Vehiculo",
            "Placa",
            "Uso",
            "Vigencia",
            "Estado",
            "Acciones",
        ])
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table.setStyleSheet("""
            QTableWidget{
                background:#0F172A;
                border:none;
                gridline-color:#172B4D;
                color:#E2E8F0;
                font-size:13px;
            }
            QTableWidget::item{
                border-bottom:1px solid #1F2937;
                padding:7px;
            }
            QHeaderView::section{
                background:#0F172A;
                border:none;
                border-bottom:1px solid #1F2937;
                padding:12px 7px;
                font-weight:700;
                color:#A5B4FC;
            }
        """)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(7, 90)
        self.table.setMinimumHeight(410)

        card_layout.addLayout(filtros_layout)
        card_layout.addWidget(self.total)
        card_layout.addWidget(self.table)
        card.setLayout(card_layout)

        main_layout.addLayout(encabezado)
        main_layout.addWidget(card)
        self.setLayout(main_layout)

    def cargar_tarjetas(self):
        self.tarjetas = obtener_tarjetas()
        self.configurar_combos()
        self.aplicar_filtros()

    def refresh_data(self):
        self.cargar_tarjetas()

    def configurar_combos(self):
        estados = sorted({dato(t, "estado", "nombre_estado") for t in self.tarjetas if dato(t, "estado", "nombre_estado")})
        usos = sorted({dato(t, "uso", "nombre_uso") for t in self.tarjetas if dato(t, "uso", "nombre_uso")})

        self.combo_estado.blockSignals(True)
        self.combo_uso.blockSignals(True)
        self.combo_estado.clear()
        self.combo_uso.clear()
        self.combo_estado.addItems(["Todos los estados"] + estados)
        self.combo_uso.addItems(["Todos los usos"] + usos)
        self.combo_estado.blockSignals(False)
        self.combo_uso.blockSignals(False)

    def aplicar_filtros(self):
        busqueda = self.input_busqueda.text().strip().lower()
        estado = self.combo_estado.currentText()
        uso = self.combo_uso.currentText()

        filtradas = []
        for tarjeta in self.tarjetas:
            texto = " ".join([
                dato(tarjeta, "codigo_identificador"),
                dato(tarjeta, "propietario", "nombre"),
                dato(tarjeta, "propietario", "nit"),
                dato(tarjeta, "vehiculo", "placa"),
                dato(tarjeta, "vehiculo", "vin"),
            ]).lower()

            coincide_busqueda = not busqueda or busqueda in texto
            coincide_estado = estado == "Todos los estados" or dato(tarjeta, "estado", "nombre_estado") == estado
            coincide_uso = uso == "Todos los usos" or dato(tarjeta, "uso", "nombre_uso") == uso

            if coincide_busqueda and coincide_estado and coincide_uso:
                filtradas.append(tarjeta)

        self.tarjetas_filtradas = filtradas
        self.pintar_tabla()

    def pintar_tabla(self):
        self.table.setRowCount(len(self.tarjetas_filtradas))

        for fila, tarjeta in enumerate(self.tarjetas_filtradas):
            marca = dato(tarjeta, "vehiculo", "linea", "marca", "nombre_marca")
            linea = dato(tarjeta, "vehiculo", "linea", "nombre_linea")
            vehiculo = f"{marca} {linea}".strip()
            detalle_vehiculo = f"{dato(tarjeta, 'vehiculo', 'modelo')} - {dato(tarjeta, 'vehiculo', 'color', 'nombre_color')}"

            valores = [
                dato(tarjeta, "codigo_identificador"),
                f"{dato(tarjeta, 'propietario', 'nombre')}\nNIT: {dato(tarjeta, 'propietario', 'nit')}",
                f"{vehiculo}\n{detalle_vehiculo}",
                dato(tarjeta, "vehiculo", "placa"),
                dato(tarjeta, "uso", "nombre_uso"),
                dato(tarjeta, "vigencia"),
                dato(tarjeta, "estado", "nombre_estado"),
            ]

            for columna, valor in enumerate(valores):
                item = QTableWidgetItem(valor)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                item.setForeground(QColor("#E2E8F0"))
                if columna in (1, 2):
                    item.setForeground(QColor("#A5B4FC"))
                self.table.setItem(fila, columna, item)

            self.table.setCellWidget(fila, 4, self.badge(dato(tarjeta, "uso", "nombre_uso"), "#FFFFFF", "#CBD5E1", "#0F172A"))
            self.table.setCellWidget(fila, 6, self.badge_estado(dato(tarjeta, "estado", "nombre_estado")))
            self.table.setCellWidget(fila, 7, self.acciones_widget(tarjeta))
            self.table.setRowHeight(fila, 50)

        self.total.setText(f"Mostrando {len(self.tarjetas_filtradas)} de {len(self.tarjetas)} tarjetas")

    def badge(self, texto, fondo, borde, color):
        contenedor = QFrame()
        contenedor.setStyleSheet("border:none; background:transparent;")
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel(texto)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(f"""
            QLabel{{
                background:{fondo};
                border:1px solid {borde};
                border-radius:10px;
                color:{color};
                padding:3px 10px;
                font-size:12px;
            }}
        """)

        layout.addWidget(label)
        contenedor.setLayout(layout)
        return contenedor

    def badge_estado(self, estado):
        estado_limpio = (estado or "").lower()
        if estado_limpio == "activa":
            return self.badge(estado, "#4ADE80", "#4ADE80", "white")
        if "vencida" in estado_limpio:
            return self.badge(estado, "#F472B6", "#F472B6", "white")
        if "suspendida" in estado_limpio:
            return self.badge(estado, "#FACC15", "#FACC15", "#0F172A")
        return self.badge(estado, "#1F2937", "#1F2937", "#94A3B8")

    def acciones_widget(self, tarjeta):
        contenedor = QFrame()
        contenedor.setStyleSheet("border:none; background:transparent;")
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_ver = QPushButton("Ver")
        btn_ver.setToolTip("Ver detalle")
        btn_ver.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_ver.setFixedSize(32, 30)
        btn_ver.setStyleSheet("""
            QPushButton{
                border:none;
                background:transparent;
                color:#7DD3FC;
                font-size:12px;
                font-weight:700;
            }
            QPushButton:hover{color:#60A5FA;}
        """)
        btn_ver.clicked.connect(lambda: self.mostrar_detalle(tarjeta))

        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.setToolTip("Eliminar tarjeta")
        btn_eliminar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_eliminar.setFixedSize(55, 30)
        btn_eliminar.setStyleSheet("""
            QPushButton{
                border:none;
                background:transparent;
                color:#F97316;
                font-size:12px;
                font-weight:700;
            }
            QPushButton:hover{color:#EA580C;}
        """)
        btn_eliminar.clicked.connect(lambda: self.eliminar_tarjeta_action(tarjeta))

        layout.addWidget(btn_ver)
        layout.addWidget(btn_eliminar)
        contenedor.setLayout(layout)
        return contenedor

    def eliminar_tarjeta_action(self, tarjeta):
        reply = QMessageBox.question(
            self,
            "Confirmar Eliminacion",
            f"¿Esta seguro que desea eliminar la tarjeta {dato(tarjeta, 'codigo_identificador')}?\nEsta accion no se puede deshacer.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                eliminar_tarjeta(dato(tarjeta, "id_tarjeta"))
                QMessageBox.information(self, "Exito", "Tarjeta eliminada correctamente.")
                self.refresh_data()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar la tarjeta:\n{str(e)}")

    def mostrar_detalle(self, tarjeta):
        modal = ModalDetalleTarjeta(tarjeta, self)
        modal.exec()

    def abrir_nueva_tarjeta(self):
        if self.navigate:
            self.navigate(2)
        elif self.stack:
            self.stack.setCurrentIndex(2)
