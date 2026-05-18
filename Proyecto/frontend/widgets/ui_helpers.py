from PyQt6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
)
from PyQt6.QtCore import Qt


PAGE_BG = "#08111F"
TEXT = "#E2E8F0"
MUTED = "#94A3B8"
BLUE = "#2563EB"
GREEN = "#4ADE80"
BORDER = "#1F2937"


def clear_layout(layout):
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget:
            widget.deleteLater()
        child = item.layout()
        if child:
            clear_layout(child)


def page_title(title, subtitle):
    box = QFrame()
    box.setStyleSheet("border:none; background:transparent;")
    layout = QHBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)

    back = QLabel("<")
    back.setStyleSheet("font-size:22px; color:#E2E8F0; border:none; background:transparent;")

    title_label = QLabel(title)
    title_label.setStyleSheet(f"font-size:23px; font-weight:800; color:{TEXT}; border:none; background:transparent;")
    subtitle_label = QLabel(subtitle)
    subtitle_label.setStyleSheet(f"font-size:15px; color:{MUTED}; border:none; background:transparent;")

    from PyQt6.QtWidgets import QVBoxLayout
    v = QFrame()
    v.setStyleSheet("border:none; background:transparent;")
    v_layout = QVBoxLayout()
    v_layout.setContentsMargins(0, 0, 0, 0)
    v_layout.addWidget(title_label)
    v_layout.addWidget(subtitle_label)
    v.setLayout(v_layout)

    layout.addWidget(back)
    layout.addSpacing(16)
    layout.addWidget(v)
    layout.addStretch()
    box.setLayout(layout)
    return box


def card():
    frame = QFrame()
    frame.setStyleSheet(f"""
        QFrame{{
            background:#0F172A;
            border:1px solid {BORDER};
            border-radius:14px;
        }}
    """)
    return frame


def input_field(placeholder=""):
    field = QLineEdit()
    field.setPlaceholderText(placeholder)
    field.setFixedHeight(34)
    field.setStyleSheet(f"""
        QLineEdit{{
            background:#0E1726;
            border:1px solid {BORDER};
            border-radius:8px;
            padding:0 12px;
            color:{TEXT};
            font-size:13px;
        }}
        QLineEdit:hover{{border:1px solid {BLUE};}}
    """)
    return field


def text_area(placeholder=""):
    area = QTextEdit()
    area.setPlaceholderText(placeholder)
    area.setFixedHeight(60)
    area.setStyleSheet(f"""
        QTextEdit{{
            background:#0E1726;
            border:1px solid {BORDER};
            border-radius:8px;
            padding:8px 10px;
            color:{TEXT};
            font-size:13px;
        }}
        QTextEdit:hover{{border:1px solid {BLUE};}}
    """)
    return area


def combo(items=None):
    cb = QComboBox()
    cb.setFixedHeight(34)
    cb.setStyleSheet(f"""
        QComboBox{{
            background:#0E1726;
            border:1px solid {BORDER};
            border-radius:8px;
            padding:7px 12px;
            color:{TEXT};
            font-size:13px;
        }}
        QComboBox:hover{{border:1px solid {BLUE};}}
        QComboBox::drop-down{{border:none; width:24px;}}
        QComboBox QAbstractItemView{{
            background:#0F172A;
            color:{TEXT};
            border:1px solid {BORDER};
            selection-background-color:#17324B;
            selection-color:{TEXT};
            outline:none;
        }}
    """)
    if items:
        cb.addItems(items)
    return cb


def primary_button(text):
    btn = QPushButton(text)
    btn.setFixedHeight(34)
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    btn.setStyleSheet(f"""
        QPushButton{{
            background:#2563EB;
            color:#E2E8F0;
            border:none;
            border-radius:8px;
            padding:0 16px;
            font-weight:700;
        }}
        QPushButton:hover{{background:#1D4ED8;}}
        QPushButton:disabled{{background:#93C5FD;}}
    """)
    return btn


def secondary_button(text):
    btn = QPushButton(text)
    btn.setFixedHeight(34)
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    btn.setStyleSheet(f"""
        QPushButton{{
            background:#111827;
            color:{TEXT};
            border:1px solid #334155;
            border-radius:8px;
            padding:0 16px;
            font-weight:600;
        }}
        QPushButton:hover{{background:#1E293B; border:1px solid {BLUE};}}
    """)
    return btn


def danger_button(text):
    btn = primary_button(text)
    btn.setStyleSheet("""
        QPushButton{
            background:#DC2626;
            color:white;
            border:none;
            border-radius:8px;
            padding:0 16px;
            font-weight:700;
        }
        QPushButton:hover{background:#B91C1C;}
    """)
    return btn


def label(text, bold=False, muted=False):
    w = QLabel(text)
    weight = "700" if bold else "400"
    color = MUTED if muted else TEXT
    w.setStyleSheet(f"font-size:13px; font-weight:{weight}; color:{color}; border:none; background:transparent;")
    return w


def badge(text, color=GREEN):
    w = QLabel(text)
    w.setAlignment(Qt.AlignmentFlag.AlignCenter)
    fg = "#111827" if color == "#FFFF99" else "white"
    w.setStyleSheet(f"""
        QLabel{{
            background:{color};
            color:{fg};
            border:none;
            border-radius:10px;
            padding:3px 9px;
            font-weight:700;
            font-size:12px;
        }}
    """)
    return w


def estado_color(estado):
    estado = (estado or "").strip().lower()
    if estado == "activa":
        return "#4ADE80"
    if "vencida" in estado:
        return "#F472B6"
    if "suspendida" in estado:
        return "#FACC15"
    return "#1F2937"
