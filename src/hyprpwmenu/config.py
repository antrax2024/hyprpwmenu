import os
import sys
from confz import BaseConfig, FileSource
from .constants import APP_NAME
import importlib.resources


def createConfigFile(configFile: str, type: str = "config") -> None:
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

            # Get the file content from package resources
            source_file = "config.yaml" if type == "config" else "style.css"
            # Use importlib.resources to get asset path
            with (
                importlib.resources.files("hyprpwmenu")
                .joinpath(f"assets/{source_file}")
                .open("rb") as src_file
            ):
                with open(configFile, "wb") as dst_file:
                    dst_file.write(src_file.read())

    except Exception as e:
        print(f"Error creating config file: {e}")
        sys.exit(1)


# Shutdown icon and command
class Shutdown(BaseConfig):
    icon: str
    command: str


# Reboot icon and command
class Reboot(BaseConfig):
    icon: str
    command: str


# Logoff icon and command
class Logoff(BaseConfig):
    icon: str
    command: str


# Main configuration class
class AppConfig(BaseConfig):
    CONFIG_SOURCES = FileSource(
        file=os.path.join(
            os.path.expanduser(path="~"), ".config", f"{APP_NAME}", "config.yaml"
        )
    )

    shutdown: Shutdown  # Shutdown icon and command
    logoff: Logoff  # Logoff icon and command
    reboot: Reboot  # Reboot icon and command


if __name__ == "__main__":
    pass
