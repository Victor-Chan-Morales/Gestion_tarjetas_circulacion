from PyQt6.QtWidgets import QFrame, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt


class Sidebar(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(240)
        self.buttons = []
        self.setStyleSheet("background-color:#091826; color:#E2E8F0;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 12, 10, 14)
        layout.setSpacing(6)

        header = QFrame()
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(10, 0, 10, 12)

        logo = QLabel("🚗")
        logo.setFixedSize(36, 30)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet("""
            background:#2563EB;
            color:#E2E8F0;
            border-radius:9px;
            font-size:12px;
            font-weight:800;
        """)

        texto_header = QVBoxLayout()
        title = QLabel("Gestión de tarjetas")
        title.setStyleSheet("font-size:14px; font-weight:700; color:#E2E8F0;")
        subtitle = QLabel("Tarjetas de Circulacion")
        subtitle.setStyleSheet("font-size:12px; color:#94A3B8;")

        texto_header.addWidget(title)
        texto_header.addWidget(subtitle)
        header_layout.addWidget(logo)
        header_layout.addLayout(texto_header)
        header.setLayout(header_layout)

        layout.addWidget(header)
        layout.addSpacing(12)

        self.btn_dashboard = QPushButton("Dashboard")
        self.btn_tarjetas = QPushButton("Tarjetas")
        self.btn_nueva_tarjeta = QPushButton("Nueva Tarjeta")
        self.btn_mantenimiento = QPushButton("Mantenimiento")
        self.btn_desactivaciones = QPushButton("Desactivaciones")
        self.btn_historial = QPushButton("Historial")

        self.buttons = [
            self.btn_dashboard,
            self.btn_tarjetas,
            self.btn_nueva_tarjeta,
            self.btn_mantenimiento,
            self.btn_desactivaciones,
            self.btn_historial,
        ]

        for btn in self.buttons:
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setFixedHeight(40)
            layout.addWidget(btn)

        layout.addStretch()

        footer = QFrame()
        footer.setStyleSheet("background-color:#0F172A; border-radius:14px;")
        footer_layout = QVBoxLayout()
        footer_layout.setContentsMargins(12, 9, 12, 9)
        admin = QLabel("Victor Chan")
        admin.setStyleSheet("color:#E2E8F0; font-weight:700; font-size:12px;")
        rol = QLabel("Administrador")
        rol.setStyleSheet("color:#94A3B8; font-size:12px;")
        footer_layout.addWidget(admin)
        footer_layout.addWidget(rol)
        footer.setLayout(footer_layout)
        layout.addWidget(footer)

        self.setLayout(layout)
        self.set_active(0)

    def set_active(self, index):
        for idx, btn in enumerate(self.buttons):
            active = idx == index
            btn.setStyleSheet(f"""
                QPushButton{{
                    background-color:{'#17394D' if active else 'transparent'};
                    border:{'1px solid #2563EB' if active else '1px solid transparent'};
                    color:{'#E2E8F0' if active else '#A5B4FC'};
                    text-align:left;
                    padding-left:13px;
                    font-size:14px;
                    border-radius:10px;
                    font-weight:{'700' if active else '500'};
                }}
                QPushButton:hover{{
                    background-color:#102D4B;
                    color:white;
                    border:1px solid #1D4ED8;
                }}
            """)
