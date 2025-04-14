import sys
import qtawesome as qta
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QToolButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, Qt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control Panel")
        # Ajuste o tamanho se necessário para acomodar o novo layout dos botões
        # self.setFixedSize(300, 100)
        self.setStyleSheet("background-color: black; color: white;")

        # Layout horizontal
        layout = QHBoxLayout()

        # Ícones
        shutdownIcon = qta.icon("fa6s.power-off", color="white")
        rebootIcon = qta.icon("fa6s.repeat", color="white")
        logoffIcon = qta.icon("ri.logout-box-r-fill", color="white")

        # Tamanho do ícone (ajuste conforme necessário)
        iconSize = QSize(32, 32)  # Example size

        # Botão Shutdown
        shutdownButton = QToolButton()
        shutdownButton.setIcon(shutdownIcon)
        shutdownButton.setIconSize(iconSize)
        shutdownButton.setText("Shutdown")
        # Define o estilo para ter texto abaixo do ícone
        shutdownButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        # Remove a borda padrão para um visual mais limpo, se desejado
        shutdownButton.setStyleSheet("QToolButton { border: none; color: white; }")
        layout.addWidget(shutdownButton)

        # Botão Reboot
        rebootButton = QToolButton()
        rebootButton.setIcon(rebootIcon)
        rebootButton.setIconSize(iconSize)
        rebootButton.setText("Reboot")
        # Define o estilo para ter texto abaixo do ícone
        rebootButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        rebootButton.setStyleSheet("QToolButton { border: none; color: white; }")
        layout.addWidget(rebootButton)

        # Botão Logoff
        logoffButton = QToolButton()
        logoffButton.setIcon(logoffIcon)
        logoffButton.setIconSize(iconSize)
        logoffButton.setText("Logoff")
        # Define o estilo para ter texto abaixo do ícone
        logoffButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        logoffButton.setStyleSheet("QToolButton { border: none; color: white; }")
        layout.addWidget(logoffButton)

        # Configura o layout na janela principal
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
