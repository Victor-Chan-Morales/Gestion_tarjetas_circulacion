from PyQt6.QtWidgets import QFrame, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt


class Sidebar(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(260)
        self.buttons = []
        self.setStyleSheet("background-color:#0F131C; color:#F8FAFC; border-right: 1px solid #1E2532;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 24, 16, 20)
        layout.setSpacing(8)

        header = QFrame()
        header.setStyleSheet("border:none;")
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(8, 0, 8, 24)

        logo = QLabel("✦")
        logo.setFixedSize(42, 42)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3B82F6, stop:1 #6366F1);
            color:#FFFFFF;
            border-radius:12px;
            font-size:24px;
            font-weight:900;
        """)

        texto_header = QVBoxLayout()
        texto_header.setSpacing(0)
        title = QLabel("Registro Vehicular")
        title.setStyleSheet("font-size:18px; font-weight:800; color:#F8FAFC; letter-spacing: -0.5px;")
        subtitle = QLabel("Gestión Vehicular")
        subtitle.setStyleSheet("font-size:12px; color:#94A3B8; font-weight: 500;")

        texto_header.addWidget(title)
        texto_header.addWidget(subtitle)
        header_layout.addWidget(logo)
        header_layout.addSpacing(6)
        header_layout.addLayout(texto_header)
        header_layout.addStretch()
        header.setLayout(header_layout)

        layout.addWidget(header)
        
        lbl_menu = QLabel("MENU")
        lbl_menu.setStyleSheet("color: #475569; font-size: 11px; font-weight: 700; padding-left: 8px; margin-bottom: 4px; border:none;")
        layout.addWidget(lbl_menu)

        self.btn_dashboard = QPushButton("  Dashboard")
        self.btn_tarjetas = QPushButton("  Tarjetas")
        self.btn_nueva_tarjeta = QPushButton("  Nueva Tarjeta")
        self.btn_mantenimiento = QPushButton("  Mantenimiento")
        self.btn_desactivaciones = QPushButton("  Desactivaciones")
        self.btn_historial = QPushButton("  Historial")

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
            btn.setFixedHeight(44)
            layout.addWidget(btn)

        layout.addStretch()

        footer = QFrame()
        footer.setStyleSheet("""
            background-color:#121822; 
            border: 1px solid #1E2532;
            border-radius:14px;
        """)
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(14, 12, 14, 12)
        
        avatar = QLabel("VC")
        avatar.setFixedSize(32, 32)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet("background:#1E293B; color:#94A3B8; border-radius:16px; font-weight:700; font-size:12px;")
        
        user_info = QVBoxLayout()
        user_info.setSpacing(0)
        admin = QLabel("Victor Chan")
        admin.setStyleSheet("color:#F8FAFC; font-weight:700; font-size:13px; border:none;")
        rol = QLabel("Administrador")
        rol.setStyleSheet("color:#64748B; font-size:11px; font-weight:500; border:none;")
        user_info.addWidget(admin)
        user_info.addWidget(rol)
        
        footer_layout.addWidget(avatar)
        footer_layout.addSpacing(8)
        footer_layout.addLayout(user_info)
        footer.setLayout(footer_layout)
        layout.addWidget(footer)

        self.setLayout(layout)
        self.set_active(0)

    def set_active(self, index):
        for idx, btn in enumerate(self.buttons):
            active = idx == index
            btn.setStyleSheet(f"""
                QPushButton{{
                    background-color:{'qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgba(59, 130, 246, 0.15), stop:1 rgba(59, 130, 246, 0.05))' if active else 'transparent'};
                    border:{'1px solid rgba(59, 130, 246, 0.3)' if active else '1px solid transparent'};
                    color:{'#60A5FA' if active else '#94A3B8'};
                    text-align:left;
                    padding-left:14px;
                    font-size:14px;
                    border-radius:10px;
                    font-weight:{'700' if active else '500'};
                }}
                QPushButton:hover{{
                    background-color:{'qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgba(59, 130, 246, 0.15), stop:1 rgba(59, 130, 246, 0.05))' if active else '#1E2532'};
                    color:{'#60A5FA' if active else '#F8FAFC'};
                    border:{'1px solid rgba(59, 130, 246, 0.3)' if active else '1px solid transparent'};
                }}
            """)
