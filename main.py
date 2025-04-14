import sys
import qtawesome as qta
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QToolButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, Qt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control Panel")
        # Ajuste o tamanho da janela para acomodar apenas os ícones
        # self.setFixedSize(150, 60) # Exemplo de tamanho menor
        # A cor do texto não é mais necessária no estilo global
        self.setStyleSheet("background-color: black;")

        # Layout horizontal
        layout = QHBoxLayout()

        # Ícones
        shutdownIcon = qta.icon("fa6s.power-off", color="white")
        rebootIcon = qta.icon("fa6s.repeat", color="white")
        logoffIcon = qta.icon("ri.logout-box-r-fill", color="white")

        # Tamanho do ícone (ajuste conforme necessário)
        iconSize = QSize(120, 120)  # Exemplo de tamanho

        # Botão Shutdown
        shutdownButton = QToolButton()
        shutdownButton.setIcon(shutdownIcon)
        shutdownButton.setIconSize(iconSize)
        # Adiciona tooltip
        shutdownButton.setToolTip("Shutdown")
        # Mantém o estilo sem borda
        shutdownButton.setStyleSheet("QToolButton { border: none; }")
        layout.addWidget(shutdownButton)

        # Botão Reboot
        rebootButton = QToolButton()
        rebootButton.setIcon(rebootIcon)
        rebootButton.setIconSize(iconSize)
        # Adiciona tooltip
        rebootButton.setToolTip("Reboot")
        rebootButton.setStyleSheet("QToolButton { border: none; }")
        layout.addWidget(rebootButton)

        # Botão Logoff
        logoffButton = QToolButton()
        logoffButton.setIcon(logoffIcon)
        logoffButton.setIconSize(iconSize)
        # Adiciona tooltip
        logoffButton.setToolTip("Logoff")
        logoffButton.setStyleSheet("QToolButton { border: none; }")
        layout.addWidget(logoffButton)

        # Configura o layout na janela principal
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
