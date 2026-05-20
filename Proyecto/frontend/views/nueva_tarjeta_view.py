from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QStackedWidget, QMessageBox, QInputDialog

from services.api_client import crear_tarjeta, obtener_catalogos, vigencia_un_anio, crear_marca, crear_linea, crear_tipo_vehiculo, crear_color
from widgets.ui_helpers import BLUE, GREEN, PAGE_BG, card, combo, input_field, label, page_title, primary_button, secondary_button


class NuevaTarjetaView(QWidget):
    def __init__(self, on_created=None):
        super().__init__()
        self.on_created = on_created
        self.catalogos = obtener_catalogos()
        self.paso = 0
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet(f"background:{PAGE_BG};")
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 28, 30, 30)
        layout.setSpacing(28)

        layout.addWidget(page_title("Nueva Tarjeta de Circulacion", "Complete los datos para generar una nueva tarjeta"))
        layout.addLayout(self.steps())

        self.stack = QStackedWidget()
        self.stack.addWidget(self.paso_vehiculo())
        self.stack.addWidget(self.paso_propietario())
        self.stack.addWidget(self.paso_tarjeta())

        center = QHBoxLayout()
        center.addStretch()
        center.addWidget(self.stack)
        center.addStretch()
        layout.addLayout(center)
        layout.addStretch()
        self.setLayout(layout)
        self.refrescar_pasos()

    def steps(self):
        self.step_buttons = []
        row = QHBoxLayout()
        row.addStretch()
        for idx, text in enumerate(["Vehiculo", "Propietario", "Tarjeta"]):
            btn = secondary_button(text)
            btn.setFixedWidth(135)
            btn.clicked.connect(lambda checked=False, i=idx: self.ir_paso(i))
            self.step_buttons.append(btn)
            row.addWidget(btn)
            if idx < 2:
                row.addWidget(label("--------", muted=True))
        row.addStretch()
        return row

    def paso_vehiculo(self):
        frame = card()
        frame.setFixedWidth(720)
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 28, 30, 28)
        layout.setSpacing(18)
        layout.addWidget(label("Datos del Vehiculo", bold=True))
        layout.addWidget(label("Ingrese la informacion del vehiculo", muted=True))

        grid = QGridLayout()
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(14)

        self.vin = input_field("Ej: JTDKN3DU5A0123456")
        self.placa = input_field("Ej: 919JDN")
        self.marca = combo(["Seleccionar marca"])
        self.linea = combo(["Seleccionar linea"])
        self.modelo = input_field("Ej: 2024")
        self.tipo = combo(["Seleccionar tipo"])
        self.color = combo(["Seleccionar color"])
        self.asientos = input_field("Ej: 5")
        self.cilindros = input_field("Ej: 4")
        self.cc = input_field("Ej: 1800")
        self.ton = input_field("Ej: 1.5")
        self.ejes = input_field("2")
        self.serie = input_field("Numero de serie")
        self.chasis = input_field("Numero de chasis")
        self.motor = input_field("Numero de motor")

        self._fill_combo(self.marca, self.catalogos["marcas"], "id_marca", "nombre_marca", True)
        self._fill_combo(self.color, self.catalogos["colores"], "id_color", "nombre_color", True)
        self.marca.currentIndexChanged.connect(self.actualizar_lineas)
        self.linea.currentIndexChanged.connect(self.actualizar_tipos_por_linea)

        btn_add_marca = secondary_button("+")
        btn_add_marca.setFixedWidth(30)
        btn_add_marca.clicked.connect(self.agregar_marca)

        btn_add_linea = secondary_button("+")
        btn_add_linea.setFixedWidth(30)
        btn_add_linea.clicked.connect(self.agregar_linea)

        btn_add_tipo = secondary_button("+")
        btn_add_tipo.setFixedWidth(30)
        btn_add_tipo.clicked.connect(self.agregar_tipo)

        btn_add_color = secondary_button("+")
        btn_add_color.setFixedWidth(30)
        btn_add_color.clicked.connect(self.agregar_color)

        self._add_field(grid, 0, 0, "VIN (Numero de Identificacion)", self.vin, 2)
        self._add_field(grid, 0, 2, "Placa sin prefijo", self.placa, 2)
        self._add_field(grid, 2, 0, "Marca", self.marca, extra_widget=btn_add_marca)
        self._add_field(grid, 2, 1, "Linea", self.linea, extra_widget=btn_add_linea)
        self._add_field(grid, 2, 2, "Modelo (Ano)", self.modelo, 2)
        self._add_field(grid, 4, 0, "Tipo de Vehiculo", self.tipo, extra_widget=btn_add_tipo)
        self._add_field(grid, 4, 1, "Color", self.color, extra_widget=btn_add_color)
        self._add_field(grid, 4, 2, "Asientos", self.asientos, 2)
        self._add_field(grid, 6, 0, "Cilindros", self.cilindros)
        self._add_field(grid, 6, 1, "Cilindrada (CC)", self.cc)
        self._add_field(grid, 6, 2, "Tonelaje", self.ton)
        self._add_field(grid, 6, 3, "Ejes", self.ejes)
        self._add_field(grid, 8, 0, "Serie", self.serie)
        self._add_field(grid, 8, 1, "Chasis", self.chasis)
        self._add_field(grid, 8, 2, "Motor", self.motor, 2)

        actions = QHBoxLayout()
        actions.addStretch()
        btn = primary_button("Continuar")
        btn.clicked.connect(lambda: self.ir_paso(1))
        actions.addWidget(btn)

        layout.addLayout(grid)
        layout.addLayout(actions)
        frame.setLayout(layout)
        self.actualizar_lineas()
        return frame

    def paso_propietario(self):
        frame = card()
        frame.setFixedWidth(720)
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 28, 30, 28)
        layout.setSpacing(16)
        layout.addWidget(label("Datos del Propietario", bold=True))
        layout.addWidget(label("Seleccione o registre un propietario", muted=True))

        self.propietario_existente = combo(["Seleccionar propietario existente"])
        self._fill_combo(self.propietario_existente, self.catalogos["propietarios"], "id_propietario", "nombre", True)
        self.nombre_propietario = input_field("Nombre del propietario")
        self.nit = input_field("Ej: 1234567-8")
        self.cui = input_field("Ej: 1234567890101")
        self.propietario_existente.currentIndexChanged.connect(self.cargar_propietario)

        self.buscar_nit = input_field("Ingrese NIT a buscar...")
        self.btn_buscar_nit = secondary_button("Buscar")
        self.btn_buscar_nit.clicked.connect(self.buscar_propietario_por_nit)

        grid = QGridLayout()
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(14)
        self._add_field(grid, 0, 0, "Buscar por NIT", self.buscar_nit, extra_widget=self.btn_buscar_nit)
        self._add_field(grid, 0, 2, "Propietario Existente", self.propietario_existente, 2)
        grid.addWidget(label("--------------  O REGISTRAR NUEVO PROPIETARIO  --------------", muted=True), 2, 0, 1, 4)
        self._add_field(grid, 3, 0, "Nombre Completo", self.nombre_propietario, 4)
        self._add_field(grid, 5, 0, "NIT", self.nit, 2)
        self._add_field(grid, 5, 2, "CUI (DPI)", self.cui, 2)

        actions = QHBoxLayout()
        atras = secondary_button("Atras")
        atras.clicked.connect(lambda: self.ir_paso(0))
        continuar = primary_button("Continuar")
        continuar.clicked.connect(lambda: self.ir_paso(2))
        actions.addWidget(atras)
        actions.addStretch()
        actions.addWidget(continuar)
        layout.addLayout(grid)
        layout.addLayout(actions)

        layout.addStretch()

        frame.setLayout(layout)
        return frame

    def paso_tarjeta(self):
        frame = card()
        frame.setFixedWidth(720)
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 28, 30, 28)
        layout.setSpacing(18)
        layout.addWidget(label("Datos de la Tarjeta", bold=True))
        layout.addWidget(label("Configure los detalles de la tarjeta", muted=True))

        grid = QGridLayout()
        grid.setHorizontalSpacing(18)
        self.uso = combo(["Seleccionar uso"])
        self._fill_combo(self.uso, self.catalogos["usos"], "id_uso", "nombre_uso", True)
        self.uso.currentIndexChanged.connect(self.actualizar_resumen)
        self.vigencia = input_field("")
        self.vigencia.setText(vigencia_un_anio())
        self.vigencia.setEnabled(False)
        self._add_field(grid, 0, 0, "Uso del Vehiculo", self.uso, 2)
        self._add_field(grid, 0, 2, "Vigencia", self.vigencia, 2)

        resumen = card()
        resumen_layout = QGridLayout()
        resumen_layout.setContentsMargins(16, 14, 16, 14)
        self.res_vin = label("-")
        self.res_placa = label("-")
        self.res_prop = label("-")
        self.res_uso = label("-")
        resumen_layout.addWidget(label("Resumen de la Tarjeta", bold=True), 0, 0, 1, 4)
        resumen_layout.addWidget(label("VIN:", muted=True), 1, 0)
        resumen_layout.addWidget(self.res_vin, 1, 1)
        resumen_layout.addWidget(label("Placa:", muted=True), 1, 2)
        resumen_layout.addWidget(self.res_placa, 1, 3)
        resumen_layout.addWidget(label("Propietario:", muted=True), 2, 0)
        resumen_layout.addWidget(self.res_prop, 2, 1)
        resumen_layout.addWidget(label("Uso:", muted=True), 2, 2)
        resumen_layout.addWidget(self.res_uso, 2, 3)
        resumen.setLayout(resumen_layout)

        for field in [self.vin, self.placa, self.nombre_propietario]:
            field.textChanged.connect(self.actualizar_resumen)

        actions = QHBoxLayout()
        atras = secondary_button("Atras")
        atras.clicked.connect(lambda: self.ir_paso(1))
        generar = primary_button("Generar Tarjeta")
        generar.clicked.connect(self.generar_tarjeta)
        actions.addWidget(atras)
        actions.addStretch()
        actions.addWidget(generar)

        layout.addLayout(grid)
        layout.addWidget(label("La placa se guardara con prefijo P- o C- segun el uso.", muted=True))
        layout.addWidget(resumen)
        layout.addLayout(actions)
        
        layout.addStretch()

        frame.setLayout(layout)
        return frame

    def _add_field(self, grid, row, col, text, widget, span=1, extra_widget=None):
        grid.addWidget(label(text), row, col, 1, span)
        if extra_widget:
            ly = QHBoxLayout()
            ly.setContentsMargins(0, 0, 0, 0)
            ly.addWidget(widget)
            ly.addWidget(extra_widget)
            grid.addLayout(ly, row + 1, col, 1, span)
        else:
            grid.addWidget(widget, row + 1, col, 1, span)

    def _fill_combo(self, cb, data, id_key, text_key, keep_first=False):
        first = cb.itemText(0) if keep_first and cb.count() else None
        cb.clear()
        if first:
            cb.addItem(first, None)
        for row in data:
            cb.addItem(row[text_key], row[id_key])

    def actualizar_lineas(self):
        marca_id = self.marca.currentData()
        self.linea.blockSignals(True)
        self.linea.clear()
        self.linea.addItem("Seleccionar linea", None)
        for linea in self.catalogos["lineas"]:
            if marca_id is None or linea["id_marca"] == marca_id:
                self.linea.addItem(linea["nombre_linea"], linea["id_linea"])
        self.linea.blockSignals(False)
        self.actualizar_tipos_por_linea()

    def actualizar_tipos_por_linea(self):
        permitidos = self.tipos_permitidos(self.linea.currentText())
        self.tipo.clear()
        self.tipo.addItem("Seleccionar tipo", None)
        for tipo in self.catalogos["tipos"]:
            if not permitidos or tipo["nombre_tipo"].lower() in permitidos:
                self.tipo.addItem(tipo["nombre_tipo"], tipo["id_tipo"])

    def tipos_permitidos(self, linea):
        linea = (linea or "").strip().lower()
        reglas = {
            "hilux": {"pick up"},
            "ranger": {"pick up"},
            "corolla": {"sedan"},
            "civic": {"sedan", "hatchback"},
            "cr-v": {"suv"},
            "crv": {"suv"},
            "accord": {"sedan"},
            "fit": {"hatchback"},
            "sentra": {"sedan"},
            "spark": {"hatchback"},
            "tucson": {"suv"},
            "cx-5": {"suv"},
            "mazda 3": {"sedan", "hatchback"},
            "mazda3": {"sedan", "hatchback"},
        }
        for clave, tipos in reglas.items():
            if clave in linea:
                return tipos
        return set()

    def cargar_propietario(self):
        propietario_id = self.propietario_existente.currentData()
        if not propietario_id:
            return
        propietario = next((p for p in self.catalogos["propietarios"] if p["id_propietario"] == propietario_id), None)
        if propietario:
            self.nombre_propietario.setText(propietario["nombre"])
            self.nit.setText(propietario["nit"])
            self.cui.setText(propietario["cui"])

    def buscar_propietario_por_nit(self):
        nit_buscado = self.buscar_nit.text().strip()
        if not nit_buscado:
            QMessageBox.warning(self, "Atencion", "Ingrese un NIT para buscar.")
            return
        prop = next((p for p in self.catalogos["propietarios"] if p["nit"] == nit_buscado), None)
        if prop:
            idx = self.propietario_existente.findData(prop["id_propietario"])
            if idx >= 0:
                self.propietario_existente.setCurrentIndex(idx)
                QMessageBox.information(self, "Encontrado", f"Propietario encontrado: {prop['nombre']}")
        else:
            QMessageBox.warning(self, "No encontrado", "No se encontro ningun propietario con ese NIT.")

    def ir_paso(self, paso):
        if paso > self.paso:
            try:
                if self.paso == 0:
                    self.validar_vehiculo()
                if self.paso == 1:
                    self.validar_propietario()
                if self.paso == 0 and paso == 2:
                    self.validar_propietario()
            except ValueError as e:
                QMessageBox.warning(self, "Campos incompletos", str(e))
                return

        self.paso = paso
        self.stack.setCurrentIndex(paso)
        if paso == 2:
            self.actualizar_resumen()
        self.refrescar_pasos()

    def refrescar_pasos(self):
        for idx, btn in enumerate(self.step_buttons):
            color = BLUE if idx == self.paso else GREEN if idx < self.paso else "#1F2937"
            text_color = "white" if idx <= self.paso else "#94A3B8"
            btn.setStyleSheet(f"""
                QPushButton{{
                    background:{color};
                    color:{text_color};
                    border:none;
                    border-radius:17px;
                    padding:0 14px;
                    font-weight:700;
                }}
            """)

    def placa_final(self):
        raw = self.placa.text().strip().upper().replace(" ", "")
        if not raw:
            return ""
        if raw.startswith(("P-", "C-")):
            return raw
        prefijo = "C" if self.uso.currentText().strip().lower() == "comercial" else "P"
        return f"{prefijo}-{raw}"

    def actualizar_resumen(self):
        self.res_vin.setText(self.vin.text() or "-")
        self.res_placa.setText(self.placa_final() or "-")
        self.res_prop.setText(self.nombre_propietario.text() or "-")
        self.res_uso.setText(self.uso.currentText() if self.uso.currentData() else "-")

    def generar_tarjeta(self):
        try:
            self.validar_formulario()
            
            confirm = QMessageBox.question(
                self, "Confirmar Generacion", 
                "¿Esta seguro que desea generar esta tarjeta con los datos ingresados?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if confirm != QMessageBox.StandardButton.Yes:
                return
                
            payload = {
                "id_propietario": self.propietario_existente.currentData(),
                "propietario": {
                    "nombre": self.nombre_propietario.text().strip(),
                    "nit": self.nit.text().strip(),
                    "cui": self.cui.text().strip(),
                },
                "id_uso": self.uso.currentData(),
                "vehiculo": {
                    "vin": self.vin.text().strip().upper(),
                    "placa": self.placa_final(),
                    "id_linea": self.linea.currentData(),
                    "modelo": int(self.modelo.text()),
                    "id_tipo": self.tipo.currentData(),
                    "id_color": self.color.currentData(),
                    "asientos": int(self.asientos.text()),
                    "ejes": int(self.ejes.text()),
                    "cilindros": int(self.cilindros.text()),
                    "cc": int(self.cc.text()),
                    "ton": float(self.ton.text() or 0),
                    "serie": self.serie.text().strip(),
                    "chasis": self.chasis.text().strip(),
                    "motor": self.motor.text().strip(),
                },
            }
            crear_tarjeta(payload)
            QMessageBox.information(self, "Tarjeta creada", "La tarjeta fue generada correctamente.")
            self.limpiar_formulario()
            if self.on_created:
                self.on_created()
        except Exception as exc:
            QMessageBox.warning(self, "No se pudo crear", f"Revise los datos o el backend.\n{exc}")

    def validar_vehiculo(self):
        for campo, nombre in [
            (self.vin, "VIN"), (self.placa, "Placa"), (self.modelo, "Modelo"),
            (self.asientos, "Asientos"), (self.ejes, "Ejes"), (self.cilindros, "Cilindros"),
            (self.cc, "Cilindrada"), (self.motor, "Motor"),
        ]:
            if not campo.text().strip():
                raise ValueError(f"Complete el campo {nombre}.")

        if len(self.vin.text().strip()) != 17:
            raise ValueError("El VIN debe tener exactamente 17 caracteres.")
        if self.placa.text().strip().upper().startswith(("P-", "C-")):
            raise ValueError("Ingrese la placa sin prefijo. El sistema agregara P- o C- segun el uso.")
        if len(self.placa.text().strip().replace(" ", "")) < 4:
            raise ValueError("Ingrese un numero de placa valido.")

        for cb, nombre in [
            (self.marca, "Marca"), (self.linea, "Linea"), (self.tipo, "Tipo de Vehiculo"),
            (self.color, "Color"),
        ]:
            if cb.currentData() is None:
                raise ValueError(f"Seleccione {nombre}.")

        try:
            modelo = int(self.modelo.text())
            if modelo < 1900 or modelo > 2100:
                raise ValueError("El modelo debe estar entre 1900 y 2100.")
        except ValueError:
            raise ValueError("El modelo debe ser un numero valido.")
            
        for campo, nombre in [(self.asientos, "asientos"), (self.ejes, "ejes"), (self.cilindros, "cilindros"), (self.cc, "cilindrada")]:
            try:
                if int(campo.text()) <= 0:
                    raise ValueError(f"El campo {nombre} debe ser mayor que cero.")
            except ValueError:
                raise ValueError(f"El campo {nombre} debe ser un numero valido.")
                
        try:
            if float(self.ton.text() or 0) < 0:
                raise ValueError("El tonelaje no puede ser negativo.")
        except ValueError:
            raise ValueError("El tonelaje debe ser un numero valido.")

    def validar_propietario(self):
        if not self.propietario_existente.currentData():
            for campo, nombre in [(self.nombre_propietario, "Nombre del propietario"), (self.nit, "NIT"), (self.cui, "CUI")]:
                if not campo.text().strip():
                    raise ValueError(f"Complete el campo {nombre}.")

    def validar_formulario(self):
        self.validar_vehiculo()
        self.validar_propietario()
        if self.uso.currentData() is None:
            raise ValueError("Seleccione Uso del Vehiculo.")

    def agregar_marca(self):
        text, ok = QInputDialog.getText(self, "Nueva Marca", "Nombre de la marca:")
        if ok and text.strip():
            try:
                crear_marca(text)
                self.refresh_data()
                QMessageBox.information(self, "Exito", "Marca agregada correctamente.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"No se pudo agregar la marca: {e}")

    def agregar_linea(self):
        marca_id = self.marca.currentData()
        if not marca_id:
            QMessageBox.warning(self, "Atencion", "Debe seleccionar una marca primero.")
            return
        text, ok = QInputDialog.getText(self, "Nueva Linea", "Nombre de la linea:")
        if ok and text.strip():
            try:
                crear_linea(marca_id, text)
                self.refresh_data()
                self.marca.setCurrentIndex(self.marca.findData(marca_id))
                QMessageBox.information(self, "Exito", "Linea agregada correctamente.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"No se pudo agregar la linea: {e}")

    def agregar_tipo(self):
        text, ok = QInputDialog.getText(self, "Nuevo Tipo", "Nombre del tipo de vehiculo:")
        if ok and text.strip():
            try:
                crear_tipo_vehiculo(text)
                self.refresh_data()
                QMessageBox.information(self, "Exito", "Tipo agregado correctamente.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"No se pudo agregar el tipo: {e}")

    def agregar_color(self):
        text, ok = QInputDialog.getText(self, "Nuevo Color", "Nombre del color:")
        if ok and text.strip():
            try:
                crear_color(text)
                self.refresh_data()
                QMessageBox.information(self, "Exito", "Color agregado correctamente.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"No se pudo agregar el color: {e}")

    def limpiar_formulario(self):
        for campo in [
            self.vin, self.placa, self.modelo, self.asientos, self.ejes, self.cilindros,
            self.cc, self.ton, self.serie, self.chasis, self.motor,
            self.nombre_propietario, self.nit, self.cui, self.buscar_nit
        ]:
            campo.clear()
        for cb in [self.marca, self.linea, self.tipo, self.color, self.propietario_existente, self.uso]:
            cb.setCurrentIndex(0)
        self.ir_paso(0)

    def refresh_data(self):
        self.catalogos = obtener_catalogos()
        if hasattr(self, "marca"):
            self._fill_combo(self.marca, self.catalogos["marcas"], "id_marca", "nombre_marca", True)
            self._fill_combo(self.color, self.catalogos["colores"], "id_color", "nombre_color", True)
            self._fill_combo(self.propietario_existente, self.catalogos["propietarios"], "id_propietario", "nombre", True)
            self._fill_combo(self.uso, self.catalogos["usos"], "id_uso", "nombre_uso", True)
            self.actualizar_lineas()
