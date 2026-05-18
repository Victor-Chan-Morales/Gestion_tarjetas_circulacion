from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QStackedWidget
)

from widgets.sidebar import Sidebar

from views.dashboard_home_view import DashboardHomeView
from views.tarjetas_view import TarjetasView
from views.nueva_tarjeta_view import NuevaTarjetaView
from views.mantenimiento_view import MantenimientoView
from views.desactivaciones_view import DesactivacionesView
from views.historial_view import HistorialView


class DashboardView(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema de Tarjetas")
        self.resize(1400, 800)

        self.init_ui()

    def init_ui(self):


        # LAYOUT PRINCIPAL


        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ==========================
        # SIDEBAR
        # ==========================

        self.sidebar = Sidebar()

        # ==========================
        # STACK
        # ==========================

        self.stack = QStackedWidget()

        self.dashboard_page = DashboardHomeView()
        self.tarjetas_page = TarjetasView(self.stack, navigate=self.switch_page)
        self.nueva_tarjeta_page = NuevaTarjetaView(on_created=lambda: self.switch_page(1, refresh=True))
        self.mantenimiento_page = MantenimientoView()
        self.desactivaciones_page = DesactivacionesView()
        self.historial_page = HistorialView()

        self.stack.addWidget(self.dashboard_page)
        self.stack.addWidget(self.tarjetas_page)
        self.stack.addWidget(self.nueva_tarjeta_page)
        self.stack.addWidget(self.mantenimiento_page)
        self.stack.addWidget(self.desactivaciones_page)
        self.stack.addWidget(self.historial_page)

        # ==========================
        # EVENTOS
        # ==========================

        self.sidebar.btn_dashboard.clicked.connect(lambda: self.switch_page(0))

        self.sidebar.btn_tarjetas.clicked.connect(lambda: self.switch_page(1))

        self.sidebar.btn_nueva_tarjeta.clicked.connect(lambda: self.switch_page(2))

        self.sidebar.btn_mantenimiento.clicked.connect(lambda: self.switch_page(3))

        self.sidebar.btn_desactivaciones.clicked.connect(lambda: self.switch_page(4))

        self.sidebar.btn_historial.clicked.connect(lambda: self.switch_page(5))

        # ==========================
        # PAGINA INICIAL
        # ==========================

        self.switch_page(0)

        # ==========================
        # AGREGAR AL LAYOUT
        # ==========================

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stack)

        self.setLayout(main_layout)

    def switch_page(self, index, refresh=True):
        self.stack.setCurrentIndex(index)
        self.sidebar.set_active(index)
        if refresh:
            page = self.stack.widget(index)
            if hasattr(page, "refresh_data"):
                page.refresh_data()
