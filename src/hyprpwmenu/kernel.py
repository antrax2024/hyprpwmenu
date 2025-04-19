import os
import time
import subprocess
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QToolButton
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QKeyEvent, QIcon, QGuiApplication
from .config import APP_NAME, AppConfig
import multiprocessing
from types import SimpleNamespace
import qtawesome as qta


class MainWindow(QWidget):
    """
    Main application window displaying control buttons.
    """

    rules = SimpleNamespace(
        focus="focuswindow class:hyprpwmenu",
        floating="togglefloating",
        fullscreen="fullscreen",
        centerwindow="centerwindow 0",
    )

    def __init__(self, appConfig: AppConfig) -> None:
        """
        Initializes the main window, layout, buttons, and styles.
        """
        super().__init__()
        self.appConfig = appConfig
        self.setWindowTitle(f"{APP_NAME}")

        # Set application name and class before creating QWidget
        QGuiApplication.setApplicationName("hyprpwmenu")
        QGuiApplication.setDesktopFileName("hyprpwmenu")
        QGuiApplication.setApplicationDisplayName("hyprpwmenu")

        # List to hold the buttons for easy navigation
        self.buttons = []
        # Index of the currently focused button (still useful for arrow key logic)
        self.currentFocusIndex = 0

        # Setup UI elements
        self.setupUI()

        # Apply global styles using stylesheets
        self.applyStyles()

        # Set initial focus to the first button
        if self.buttons:
            self.buttons[self.currentFocusIndex].setFocus()

    def setupUI(self) -> None:
        """
        Sets up the user interface elements like layout and buttons.
        """
        # Horizontal layout
        layout = QHBoxLayout()
        # Remove spacing and margins for a tighter look
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Icons
        shutdownIcon = qta.icon(
            self.appConfig.shutdown.icon,
            color=self.appConfig.general.icon_color,
            color_active=self.appConfig.general.icon_color_active,
        )
        rebootIcon = qta.icon(
            self.appConfig.reboot.icon,
            color=self.appConfig.general.icon_color,
            color_active=self.appConfig.general.icon_color_active,
        )
        logoffIcon = qta.icon(
            self.appConfig.logoff.icon,
            color=self.appConfig.general.icon_color,
            color_active=self.appConfig.general.icon_color_active,
        )

        # Icon size
        iconSize = QSize(
            self.appConfig.general.icon_width, self.appConfig.general.icon_height
        )

        # Create buttons and add them to layout and list

        # shutdownButton
        shutdownButton = self.createButton("Shutdown", shutdownIcon, iconSize)
        shutdownButton.clicked.connect(self.shutdownButtonClick)
        self.buttons.append(shutdownButton)
        # rebootButton
        rebootButton = self.createButton("Reboot", rebootIcon, iconSize)
        rebootButton.clicked.connect(self.rebootButtonClick)
        self.buttons.append(rebootButton)
        # logoffButton
        logoffButton = self.createButton("Logoff", logoffIcon, iconSize)
        logoffButton.clicked.connect(self.logoffButtonClick)
        self.buttons.append(logoffButton)

        for button in self.buttons:
            layout.addWidget(button)

        # Set the layout on the main window
        self.setLayout(layout)

        # Adjusting Windows Parameters
        ## Make window floating
        floatingProcess = multiprocessing.Process(
            target=self.childDispatch, args=("'togglefloating class:^(hyprpwmenu)$'",)
        )
        floatingProcess.start()
        ## Analizing if the window is fullscreen
        if self.appConfig.main_window.fullscreen:
            print("Fullscreen mode enabled")
            # Set the window to fullscreen
            fullscreenProcess = multiprocessing.Process(
                target=self.childDispatch,
                args=(self.rules.fullscreen,),
            )
            fullscreenProcess.start()
        else:
            print("Fullscreen mode disabled")
            # Resize the window to the specified dimensions
            sizeProcess = multiprocessing.Process(
                target=self.childDispatch,
                args=(
                    f"resizeactive exact {self.appConfig.main_window.width} {self.appConfig.main_window.height}",
                ),
            )
            sizeProcess.start()
            # center the window
            centerProcess = multiprocessing.Process(
                target=self.childDispatch,
                args=(self.rules.centerwindow,),
            )
            centerProcess.start()

    def shutdownButtonClick(self) -> None:
        """
        Action performed when the shutdown button is clicked or activated.
        """
        subprocess.run(
            self.appConfig.shutdown.command,
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def rebootButtonClick(self) -> None:
        """
        Action performed when the reboot button is clicked or activated.
        """
        subprocess.run(
            self.appConfig.reboot.command,
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def logoffButtonClick(self) -> None:
        """
        Action performed when the logoff button is clicked or activated.
        """
        subprocess.run(
            self.appConfig.logoff.command,
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def createButton(self, tooltip: str, icon: QIcon, iconSize: QSize) -> QToolButton:
        """
        Creates a QToolButton with specified properties.

        Args:
            tooltip (str): The text to show when hovering over the button.
            icon (QIcon): The icon for the button (created using qtawesome).
            iconSize (QSize): The desired size of the icon.

        Returns:
            QToolButton: The configured tool button.
        """
        button = QToolButton()
        button.setIcon(icon)
        button.setIconSize(iconSize)
        button.setToolTip(tooltip)
        # Set focus policy to allow keyboard focus
        button.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        return button

    def applyStyles(self) -> None:
        """
        Applies CSS-like stylesheets for appearance and hover/focus effects.
        """
        self.setStyleSheet(
            """
            QWidget {
                background-color: %s; /* Window background */
            }
            QToolButton {
                background-color: transparent; /* Default transparent background */
                border: 2px solid transparent; /* Add transparent border to reserve space */
                border-radius: 15px; /* Rounded corners */
                padding: 5px; /* Add some padding around the icon */
                margin: 0px; /* No margin between buttons */
            }
            /* Style for when the button has keyboard focus */
            QToolButton:focus {
                border: 2px solid %s; 
                background-color: transparent; /* Slightly lighter background when focused */
            }
            /* Optional: Style for when the mouse is hovering */
            QToolButton:hover {
                background-color: #222222; /* Dark gray background on hover */
            }
            QToolTip {
                color: black;
                background-color: lightgray;
                border: 1px solid black;
            }
        """
            % (
                self.appConfig.main_window.background_color,
                self.appConfig.general.icon_color,
            )
        )

    # --- MÉTODO CORRIGIDO ---
    def keyPressEvent(self, event: QKeyEvent) -> None:  # type: ignore
        """
        Handles key press events for navigation between buttons and triggering actions.

        Args:
            event (QKeyEvent): The key event object.
        """
        key = event.key()
        numButtons = len(self.buttons)

        if not numButtons:  # Do nothing if there are no buttons
            super().keyPressEvent(event)
            return

        # Handle Escape key to exit the application
        if key == Qt.Key.Key_Escape:
            self.close()  # Close the window

        elif key == Qt.Key.Key_Right:
            # Move focus to the next button, wrap around
            self.currentFocusIndex = (self.currentFocusIndex + 1) % numButtons
            self.buttons[self.currentFocusIndex].setFocus()
        elif key == Qt.Key.Key_Left:
            # Move focus to the previous button, wrap around
            self.currentFocusIndex = (
                self.currentFocusIndex - 1 + numButtons
            ) % numButtons
            self.buttons[self.currentFocusIndex].setFocus()
        # --- CONDIÇÃO CORRIGIDA ---
        # Check for Enter key (Return on main keyboard, Enter on numpad)
        elif key == Qt.Key.Key_Return or key == Qt.Key.Key_Enter:
            # Get the widget that currently has focus within this window
            focusedWidget = self.focusWidget()
            # Check if the focused widget is one of our QToolButtons
            if isinstance(focusedWidget, QToolButton) and focusedWidget in self.buttons:
                # Trigger the click action of the actually focused button
                focusedWidget.click()  # Simulate a button click on the focused widget
            # --- FIM DA CONDIÇÃO CORRIGIDA ---
        else:
            # Handle other keys normally by passing the event to the parent
            super().keyPressEvent(event)

    def childDispatch(self, rule: str) -> None:
        # print("childDispatch started")
        time.sleep(0.1)  # Atraso de 100ms.
        # First dispatch the focus rule to ensure the window is focused
        # self.hyprctlDispatch(rule=self.rules.focus)
        # Then dispatch the actual rule
        self.hyprctlDispatch(rule=rule)
        # print("childDispatch finished")

    def hyprctlDispatch(self, rule: str) -> None:
        """
        Executes a command Dispatch using the Hyprland control tool (hyprctl).

        Args:
            rule (str): The rule to execute.
        """
        subprocess.run(
            f"hyprctl dispatch focuswindow class:hyprpwmenu ; hyprctl dispatch {rule}",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
