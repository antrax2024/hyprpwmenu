import sys
import qtawesome as qta
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control Panel")
        self.setFixedSize(300, 100)

        # Set background color to black
        self.setStyleSheet("background-color: black; color: white;")

        # Layout horizontal
        layout = QHBoxLayout()

        # Botão Shutdown
        shutdownButton = QPushButton(
            qta.icon("fa6s.power-off", color="white"), "Shutdown"
        )
        # shutdownButton.setIconSize(QSize(120, 120))
        # shutdownButton.setToolTip("Shutdown")
        layout.addWidget(shutdownButton)

        # Botão Reboot
        # Botão Shutdown
        rebootButton = QPushButton(qta.icon("fa6s.repeat", color="white"), "Reboot")
        layout.addWidget(rebootButton)

        # Botão Logoff
        logoffButton = QPushButton(
            qta.icon("ri.logout-box-r-fill", color="white"), "Logoff"
        )
        layout.addWidget(logoffButton)

        # Configura o layout na janela principal
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
