import sys
import os
from PyQt6.QtWidgets import QApplication
from views.dashboard_view import DashboardView

def main():
    app = QApplication(sys.argv)
    
    # Ruta al archivo QSS relativa al directorio de ejecución
    qss_path = os.path.join(os.path.dirname(__file__), "ui", "styles.qss")
    
    # Leer e aplicar los estilos si el archivo existe
    if os.path.exists(qss_path):
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    else:
        print(f"No se pudo encontrar el archivo de estilos en: {qss_path}")

    window = DashboardView()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()