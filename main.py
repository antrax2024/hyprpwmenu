# -*- coding: utf-8 -*-
import sys
import subprocess
import qtawesome as qta
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QSizePolicy,
)
from PyQt6.QtGui import QIcon, QKeyEvent
from PyQt6.QtCore import (
    Qt,
    QSize,
    QProcess,
)
import qdarktheme


def executeShellCommand(commandList: list[str]) -> None:
    """
    Executes a shell command using subprocess.

    Args:
        commandList: A list of strings representing the command and its arguments.

    Raises:
        RuntimeError: If the command execution fails.
    """
    try:
        # Using list format is generally safer than shell=True
        result = subprocess.run(
            args=commandList,
            check=True,
            capture_output=True,  # Captures stdout and stderr
            text=True,
        )
        print(f"Command '{' '.join(commandList)}' executed successfully.")
        print(f"Stdout: {result.stdout}")
        print(f"Stderr: {result.stderr}")
    except FileNotFoundError:
        # Handle case where the command itself isn't found
        print(f"Error: Command not found: {commandList[0]}")
        # Optionally raise or show an error dialog
        # raise RuntimeError(f"Command not found: {commandList[0]}")
    except subprocess.CalledProcessError as e:
        # Handle errors during command execution
        print(f"Error executing command '{' '.join(commandList)}':")
        print(f"Return code: {e.returncode}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        # Optionally raise or show an error dialog
        # raise RuntimeError(f"Erro no comando {' '.join(commandList)} (código {e.returncode}): {e.stderr}") from e
    except PermissionError as e:
        # Specific handling for permission issues (e.g. sudo without password)
        print(
            f"Permission denied for command: {' '.join(commandList)}. Do you need sudo rights?"
        )
        # raise RuntimeError(f"Permission denied for command: {' '.join(commandList)}") from e
    except Exception as e:
        # Catch other potential exceptions
        print(
            f"An unexpected error occurred while executing {' '.join(commandList)}: {e}"
        )
        # raise RuntimeError(f"An unexpected error occurred: {e}") from e


# --- Main Application Window ---


class PowerMenuWindow(QWidget):
    """
    Main window class for the Power Menu application.

    Inherits from QWidget and sets up the UI elements and connections.
    """

    def __init__(self):
        """
        Initializes the PowerMenuWindow.
        Sets up the window properties, layout, buttons, and signal connections.
        """
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Sets up the user interface components.
        """
        # --- Window Properties ---
        self.setWindowTitle("Power Menu")
        # Make the window frameless (removes title bar and borders)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup)

        # --- Layouts ---
        # Main vertical layout to center the button row
        mainLayout = QVBoxLayout(self)
        mainLayout.addStretch(stretch=1)  # Add space above

        # Horizontal layout for the buttons
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch(stretch=1)  # Add space to the left

        # --- Icons ---
        shutdownIcon = qta.icon("ph.power-bold")
        rebootIcon = qta.icon("ei.repeat")
        logoutIcon = qta.icon("mdi6.logout-variant")

        # --- Buttons ---
        self.shutdownButton = QPushButton(self)
        self.shutdownButton.setIcon(shutdownIcon)
        self.shutdownButton.setToolTip("Shutdown the System")
        self.shutdownButton.setFlat(True)  # Make button background transparent
        self.shutdownButton.clicked.connect(self.shutdownButtonClicked)
        self.shutdownButton.setAutoDefault(True)
        self.rebootButton = QPushButton(self)
        self.rebootButton.setIcon(rebootIcon)
        self.rebootButton.setToolTip("Reboot the System")
        self.rebootButton.setFlat(True)
        self.rebootButton.clicked.connect(self.rebootButtonClicked)
        self.rebootButton.setAutoDefault(False)

        self.logoutButton = QPushButton(self)
        self.logoutButton.setIcon(logoutIcon)
        self.logoutButton.setToolTip("Logout the User")
        self.logoutButton.setFlat(True)
        self.logoutButton.clicked.connect(self.logoutButtonClicked)
        self.logoutButton.setAutoDefault(False)

        # Add buttons to the horizontal layout
        buttonLayout.addWidget(self.shutdownButton)
        buttonLayout.addWidget(self.rebootButton)
        buttonLayout.addWidget(self.logoutButton)
        buttonLayout.addStretch(1)  # Add space to the right

        # Add button layout to the main vertical layout
        mainLayout.addLayout(buttonLayout)
        mainLayout.addStretch(1)  # Add space below

        # Set the main layout for the window
        self.setLayout(mainLayout)

        # Adjust window size to fit content snugly
        self.adjustSize()
        # Center the window on screen
        self.centerWindow()

    # --- Button Click Handlers ---
    def shutdownButtonClicked(self):
        """
        Handles the click event for the Shutdown button.
        Executes the shutdown command and closes the application window.
        """
        print("Shutdown Button Clicked")
        executeShellCommand("sudo shutdown -h now")
        self.close()  # Close the PyQt window

    def rebootButtonClicked(self):
        """
        Handles the click event for the Reboot button.
        Executes the reboot command and closes the application window.
        """
        print("Reboot Button Clicked")
        executeShellCommand("sudo reboot")
        self.close()  # Close the PyQt window

    def logoutButtonClicked(self):
        """
        Handles the click event for the Logout button.
        Executes the logout command and closes the application window.
        """
        print("Logout Button Clicked")
        executeShellCommand("hyprctl dispatch exit")
        self.close()  # Close the PyQt window

    # --- Event Handlers ---
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            print("Escape key pressed, closing window.")
            self.close()
            # Close application
            sys.exit(0)  # Exit the application completely
        else:
            # Allow processing of other keys if necessary (e.g., Tab for focus)
            super().keyPressEvent(event)

    # --- Utility Methods ---
    def centerWindow(self):
        """Centers the window on the screen."""
        frameGeometry = self.frameGeometry()
        screenCenter = self.screen().availableGeometry().center()
        frameGeometry.moveCenter(screenCenter)
        self.move(frameGeometry.topLeft())


# --- Main Execution Block ---
if __name__ == "__main__":
    # Create the QApplication instance
    app = QApplication(sys.argv)

    # config theme dark
    qdarktheme.setup_theme(theme="dark")

    # Create and show the main window
    window = PowerMenuWindow()
    window.show()

    # Start the application's event loop
    sys.exit(app.exec())
