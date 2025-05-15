import subprocess
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QHBoxLayout, QToolButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent, QGuiApplication, QFontDatabase
from .config import AppConfig
from .constants import APP_NAME, APP_VERSION
import importlib.resources


class MainWindow(QWidget):
    """
    Main application window displaying control buttons.
    """

    def __init__(self, appConfig: AppConfig, style_file: str) -> None:
        """
        Initializes the main window, layout, buttons, and styles.
        """
        super().__init__()
        self.appConfig = appConfig
        self.style_file = style_file
        self.setWindowTitle(f"{APP_NAME}")
        self.setObjectName("hyprpwmenu")

        # List to hold the buttons for easy navigation (initialize early)
        self.buttons = []
        # Index of the currently focused button (still useful for arrow key logic)
        self.currentFocusIndex = 0

        # Set application name and class before creating QWidget
        QGuiApplication.setApplicationName("hyprpwmenu")
        QGuiApplication.setDesktopFileName("hyprpwmenu")
        QGuiApplication.setApplicationDisplayName("hyprpwmenu")

        print("Loading Font Awesome font...")
        self.loadFontAwesome()

        print("Setting up UI...")
        self.setupUI()

        # Apply global styles using stylesheets
        print("Applying styles...")
        self.applyStyles()

        # Set initial focus to the first button
        if self.buttons:
            self.buttons[self.currentFocusIndex].setFocus()

    def setupUI(self) -> None:
        """
        Sets up the user interface elements like layout and buttons.
        """

        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)
        mainLayout.addStretch(1)

        # Horizontal layout
        buttonsLayout = QHBoxLayout()
        # Remove spacing and margins for a tighter look
        buttonsLayout.setContentsMargins(0, 0, 0, 0)
        buttonsLayout.setSpacing(0)

        # Create buttons and add them to layout and list
        # shutdownButton
        shutdownButton = self.createButton(
            text="Shutdown",
            icon_unicode=self.appConfig.shutdown.icon,
            objectName="shutdownButton",
        )
        shutdownButton.clicked.connect(self.shutdownButtonClick)
        self.buttons.append(shutdownButton)

        # rebootButton
        rebootButton = self.createButton(
            text="Reboot",
            icon_unicode=self.appConfig.reboot.icon,
            objectName="rebootButton",
        )
        rebootButton.clicked.connect(self.rebootButtonClick)
        self.buttons.append(rebootButton)

        # logoffButton
        logoffButton = self.createButton(
            text="Logoff",
            icon_unicode=self.appConfig.logoff.icon,
            objectName="logoffButton",
        )
        logoffButton.clicked.connect(self.logoffButtonClick)
        self.buttons.append(logoffButton)

        # Add a stretch at the beginning to center the buttons
        buttonsLayout.addStretch(1)
        # Add first button
        buttonsLayout.addWidget(shutdownButton)
        # space_between_buttons
        space_between_buttons = 35
        buttonsLayout.addSpacing(space_between_buttons)

        # Add second button
        buttonsLayout.addWidget(rebootButton)

        # Add fixed-width spacer
        buttonsLayout.addSpacing(space_between_buttons)

        # Add third button
        buttonsLayout.addWidget(logoffButton)

        # Add a stretch at the end to center the buttons
        buttonsLayout.addStretch(1)

        # add buttonsLayout to mainLayout
        mainLayout.addLayout(buttonsLayout)
        mainLayout.addStretch(1)

        # Create a label for app name and version
        appInfoLabel = QLabel(f"{APP_NAME} v{APP_VERSION}")
        appInfoLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        appInfoLabel.setObjectName("app_info_label")
        # Cria um sublayout horizontal para a label
        bottomLayout = QHBoxLayout()
        bottomLayout.addStretch(1)  # Empurra a label para a direita
        bottomLayout.addWidget(appInfoLabel)

        mainLayout.addLayout(bottomLayout)

    def loadFontAwesome(self) -> None:
        """
        Load Font Awesome 6 Free font variants from the assets directory.
        Loads Solid, Regular, and Brands versions.

        Returns:
            None
        """
        try:
            # Define paths to all three font variants
            fontPathSolid = str(
                importlib.resources.files("hyprpwmenu").joinpath(
                    "assets/Font Awesome 6 Free-Solid-900.otf"
                )
            )
            fontPathRegular = str(
                importlib.resources.files("hyprpwmenu").joinpath(
                    "assets/Font Awesome 6 Free-Regular-400.otf"
                )
            )
            fontPathBrands = str(
                importlib.resources.files("hyprpwmenu").joinpath(
                    "assets/Font Awesome 6 Brands-Regular-400.otf"
                )
            )

            # Load all font variants
            idSolid = QFontDatabase.addApplicationFont(fontPathSolid)
            idRegular = QFontDatabase.addApplicationFont(fontPathRegular)
            idBrands = QFontDatabase.addApplicationFont(fontPathBrands)

            loadingErrors = []

            # Check for loading errors
            if idSolid < 0:
                loadingErrors.append("Solid")
            if idRegular < 0:
                loadingErrors.append("Regular")
            if idBrands < 0:
                loadingErrors.append("Brands")

            if loadingErrors:
                print(
                    f"Error: Failed to load Font Awesome variants: {', '.join(loadingErrors)}"
                )
            else:
                # Get font families for each variant
                familiesSolid = QFontDatabase.applicationFontFamilies(idSolid)
                familiesRegular = QFontDatabase.applicationFontFamilies(idRegular)
                familiesBrands = QFontDatabase.applicationFontFamilies(idBrands)

                print("Font Awesome loaded successfully:")
                print(f"- Solid families: {familiesSolid}")
                print(f"- Regular families: {familiesRegular}")
                print(f"- Brands families: {familiesBrands}")

        except Exception as e:
            print(f"Error loading Font Awesome fonts: {e}")

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

    def createButton(
        self,
        text: str,
        icon_unicode: str,
        objectName: str = None,  # type: ignore
    ) -> QToolButton:
        """
        Cria um QToolButton com ícone do Font Awesome e texto.

        Args:
            icon_unicode (str): Código Unicode do ícone (ex: "\uf015" para "home").
        """
        button = QToolButton()
        button.setObjectName(objectName)
        button.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # Layout vertical para ícone e texto
        layout = QVBoxLayout(button)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(4)

        # Label do ícone (Font Awesome)
        icon_label = QLabel(icon_unicode)
        icon_label.setObjectName(f"icon{objectName}")
        layout.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Label do texto
        text_label = QLabel(text)
        text_label.setObjectName(f"text{objectName}")
        layout.addWidget(text_label, alignment=Qt.AlignmentFlag.AlignCenter)

        return button

    def applyStyles(self) -> None:
        """
        Applies CSS-like stylesheets from external CSS file.
        Dynamically replaces variables with configuration values.
        """
        # Path to CSS file (relative to the module)
        cssPath = self.style_file

        try:
            # Read CSS file content
            with open(cssPath, "r") as cssFile:
                cssContent = cssFile.read()

            # Apply the stylesheet
            self.setStyleSheet(cssContent)

        except FileNotFoundError:
            print(f"Warning: CSS file not found at {cssPath}")
            # Fallback to inline styles

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
