import sys
from ui import MainWindow
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('icon.ico'))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()