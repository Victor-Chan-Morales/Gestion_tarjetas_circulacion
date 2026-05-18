from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit
)

from datetime import datetime


class TopBar(QFrame):

    def __init__(self, titulo):
        super().__init__()

        self.titulo = titulo

        self.setFixedHeight(80)

        self.setStyleSheet("""
            background-color: #0F172A;
            border-bottom: 1px solid #1F2937;
        """)

        self.init_ui()

    def init_ui(self):

        layout = QHBoxLayout()

        # ==========================
        # TITULO
        # ==========================

        title = QLabel(self.titulo)

        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #E2E8F0;
        """)

        # ==========================
        # BUSCADOR
        # ==========================

        self.search_input = QLineEdit()

        self.search_input.setPlaceholderText(
            "Buscar..."
        )

        self.search_input.setFixedWidth(300)

        self.search_input.setStyleSheet("""
            QLineEdit{
                padding:10px;
                border:1px solid #1F2937;
                border-radius:8px;
                font-size:14px;
                background:#102134;
                color:#E2E8F0;
            }
            QLineEdit:focus{border:1px solid #2563EB;}
        """)

        # ==========================
        # FECHA
        # ==========================

        fecha = QLabel(
            datetime.now().strftime("%d/%m/%Y")
        )

        fecha.setStyleSheet("""
            color:#94A3B8;
            font-size:14px;
        """)

        # ==========================
        # LAYOUT
        # ==========================

        layout.addWidget(title)

        layout.addStretch()

        layout.addWidget(self.search_input)
        layout.addSpacing(20)
        layout.addWidget(fecha)

        self.setLayout(layout)