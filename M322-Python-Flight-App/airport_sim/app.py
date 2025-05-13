from PySide6.QtWidgets import QApplication
from views.mainwindow import MainWindow
import sys
import random

# optional – neue Zufallssaat setzen, damit jede Session anders ist
random.seed()          

def main() -> None:
    """Startet die GUI‑Anwendung."""
    app = QApplication(sys.argv)

    # Qt‑Theme – Fusion ist schlicht & plattform­übergreifend
    QApplication.setStyle("Fusion")

    window = MainWindow()
    window.showMaximized()           # startet im Maximized‑Modus
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
