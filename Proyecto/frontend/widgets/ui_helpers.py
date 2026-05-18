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


PAGE_BG = "#0B0E14"
TEXT = "#F8FAFC"
MUTED = "#94A3B8"
BLUE = "#3B82F6"
GREEN = "#10B981"
BORDER = "#1E2532"
CARD_BG = "#121822"
INPUT_BG = "#0F131C"


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

    back = QLabel("✦")
    back.setStyleSheet(f"font-size:24px; color:{BLUE}; border:none; background:transparent; font-weight:800;")

    title_label = QLabel(title)
    title_label.setStyleSheet(f"font-size:26px; font-weight:900; color:{TEXT}; border:none; background:transparent; letter-spacing: -0.5px;")
    subtitle_label = QLabel(subtitle)
    subtitle_label.setStyleSheet(f"font-size:14px; color:{MUTED}; border:none; background:transparent; font-weight: 500;")

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
            background:{CARD_BG};
            border:1px solid {BORDER};
            border-radius:16px;
        }}
    """)
    return frame


def input_field(placeholder=""):
    field = QLineEdit()
    field.setPlaceholderText(placeholder)
    field.setFixedHeight(40)
    field.setStyleSheet(f"""
        QLineEdit{{
            background:{INPUT_BG};
            border:1px solid {BORDER};
            border-radius:10px;
            padding:0 14px;
            color:{TEXT};
            font-size:14px;
            font-weight: 500;
        }}
        QLineEdit:focus{{border:1px solid {BLUE}; background: #131A26;}}
        QLineEdit:hover:!focus{{border:1px solid #2A3441;}}
    """)
    return field


def text_area(placeholder=""):
    area = QTextEdit()
    area.setPlaceholderText(placeholder)
    area.setFixedHeight(80)
    area.setStyleSheet(f"""
        QTextEdit{{
            background:{INPUT_BG};
            border:1px solid {BORDER};
            border-radius:10px;
            padding:12px 14px;
            color:{TEXT};
            font-size:14px;
            font-weight: 500;
        }}
        QTextEdit:focus{{border:1px solid {BLUE}; background: #131A26;}}
        QTextEdit:hover:!focus{{border:1px solid #2A3441;}}
    """)
    return area


def combo(items=None):
    cb = QComboBox()
    cb.setFixedHeight(40)
    cb.setStyleSheet(f"""
        QComboBox{{
            background:{INPUT_BG};
            border:1px solid {BORDER};
            border-radius:10px;
            padding:0 14px;
            color:{TEXT};
            font-size:14px;
            font-weight: 500;
        }}
        QComboBox:focus{{border:1px solid {BLUE}; background: #131A26;}}
        QComboBox:hover:!focus{{border:1px solid #2A3441;}}
        QComboBox::drop-down{{border:none; width:30px;}}
        QComboBox QAbstractItemView{{
            background:{INPUT_BG};
            color:{TEXT};
            border:1px solid {BORDER};
            border-radius:8px;
            selection-background-color:#1E293B;
            selection-color:{BLUE};
            outline:none;
        }}
    """)
    if items:
        cb.addItems(items)
    return cb


def primary_button(text):
    btn = QPushButton(text)
    btn.setFixedHeight(42)
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    btn.setStyleSheet(f"""
        QPushButton{{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3B82F6, stop:1 #6366F1);
            color:#FFFFFF;
            border:none;
            border-radius:10px;
            padding:0 20px;
            font-weight:700;
            font-size:14px;
        }}
        QPushButton:hover{{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2563EB, stop:1 #4F46E5);
        }}
        QPushButton:disabled{{background:#1E293B; color:#475569;}}
    """)
    return btn


def secondary_button(text):
    btn = QPushButton(text)
    btn.setFixedHeight(42)
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    btn.setStyleSheet(f"""
        QPushButton{{
            background:#111827;
            color:{TEXT};
            border:1px solid {BORDER};
            border-radius:10px;
            padding:0 20px;
            font-weight:600;
            font-size:14px;
        }}
        QPushButton:hover{{background:#1E293B; border:1px solid #334155; color:#FFFFFF;}}
    """)
    return btn


def danger_button(text):
    btn = QPushButton(text)
    btn.setFixedHeight(42)
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    btn.setStyleSheet("""
        QPushButton{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #EF4444, stop:1 #F43F5E);
            color:white;
            border:none;
            border-radius:10px;
            padding:0 20px;
            font-weight:700;
            font-size:14px;
        }
        QPushButton:hover{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #DC2626, stop:1 #E11D48);
        }
    """)
    return btn


def label(text, bold=False, muted=False):
    w = QLabel(text)
    weight = "700" if bold else "500"
    color = MUTED if muted else TEXT
    w.setStyleSheet(f"font-size:14px; font-weight:{weight}; color:{color}; border:none; background:transparent;")
    return w


def badge(text, color=GREEN):
    w = QLabel(text)
    w.setAlignment(Qt.AlignmentFlag.AlignCenter)
    fg = "#064E3B" if color == "#10B981" else ("#78350F" if color == "#F59E0B" else "#FFFFFF")
    w.setStyleSheet(f"""
        QLabel{{
            background:{color};
            color:{fg};
            border:none;
            border-radius:12px;
            padding:4px 12px;
            font-weight:700;
            font-size:12px;
            letter-spacing: 0.5px;
        }}
    """)
    return w


def estado_color(estado):
    estado = (estado or "").strip().lower()
    if estado == "activa":
        return "#10B981" # Emerald 500
    if "vencida" in estado:
        return "#F43F5E" # Rose 500
    if "suspendida" in estado:
        return "#F59E0B" # Amber 500
    return "#64748B" # Slate 500
