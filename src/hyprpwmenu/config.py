import os
import sys
from confz import BaseConfig, FileSource
from .constants import APP_NAME
import shutil


def createConfigFile(configFile: str) -> None:
    """
    Create the config file if it doesn't exist.
    """
    try:
        if not os.path.exists(path=configFile):
            dir_name: str = os.path.dirname(configFile)
            if dir_name:
                os.makedirs(
                    name=dir_name,
                    exist_ok=True,
                )

            # copy the file assets/config.yaml to dir_name
            shutil.copy2(src="assets/config.yaml", dst=dir_name)

    except Exception as e:
        print(f"Error creating config file: {e}")
        sys.exit(1)


# General specifications
class General(BaseConfig):
    icon_color: str  # Color of the icon
    icon_color_active: str  # Color of the icon when active
    icon_width: int  # Width of the icon
    icon_height: int  # Height of the icon
    font_size: str  # Font size for the text under the icon


# Main Window
class MainWindow(BaseConfig):
    fullscreen: bool  # Fullscreen mode
    width: int  # Width of the window
    height: int  # Height of the window
    space_between_buttons: int  # Fixed space between buttons
    background_color: str  # Background color


# Shutdown icon and command
class Shutdown(BaseConfig):
    icon: str
    icon_color: str
    command: str


# Reboot icon and command
class Reboot(BaseConfig):
    icon: str
    icon_color: str
    command: str


# Logoff icon and command
class Logoff(BaseConfig):
    icon: str
    icon_color: str
    command: str


# Main configuration class
class AppConfig(BaseConfig):

    CONFIG_SOURCES = FileSource(
        file=os.path.join(
            os.path.expanduser(path="~"), ".config", f"{APP_NAME}", "config.yaml"
        )
    )

    general: General  # General
    main_window: MainWindow  # Main Window
    shutdown: Shutdown  # Shutdown icon and command
    logoff: Logoff  # Logoff icon and command
    reboot: Reboot  # Reboot icon and command


if __name__ == "__main__":
    pass
