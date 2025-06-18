"""
Configuration Management Module for HyprPwMenu

This module handles configuration file management, including creation of default files
and loading application settings. It uses the confz library for configuration management
with YAML files and Pydantic for data validation.

Classes:
    Button: Configuration model for individual power menu buttons
    AppConfig: Main application configuration containing button definitions

Functions:
    createConfigFile: Creates default configuration or style files if they don't exist

Dependencies:
    - confz: Configuration management with YAML support
    - importlib.resources: For accessing package assets
    - os: File system operations
    - sys: System-specific parameters and functions
"""

import os
import sys
from confz import BaseConfig, FileSource
from .constants import APP_NAME
import importlib.resources
from typing import List


def createConfigFile(configFile: str, type: str = "config") -> None:
    """
    Create default configuration or style files if they don't exist.

    This function creates the necessary directory structure and copies default
    files from the package assets to the specified location.

    Args:
        configFile: Absolute path where the file should be created
        type: Type of file to create ("config" for YAML config, "style" for CSS)

    Returns:
        None: Creates file on disk

    Raises:
        SystemExit: If file creation fails due to permissions or other errors

    Side Effects:
        - Creates parent directories if they don't exist
        - Copies default files from package assets
        - Outputs error messages if creation fails

    Example:
        >>> createConfigFile("/home/user/.config/hyprpwmenu/config.yaml", "config")
        >>> createConfigFile("/home/user/.config/hyprpwmenu/style.css", "style")
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


class Button(BaseConfig):
    """
    Configuration model for individual power menu buttons.

    This class defines the structure and validation for button configurations
    used in the power menu interface. Each button represents a system action
    like shutdown, reboot, or logout.

    Attributes:
        icon_path (str): Absolute path to PNG icon file for the button
        id (str): Unique CSS identifier for styling the button element
        hint (str): Tooltip text displayed when user hovers over the button
        command (str): Shell command executed when the button is clicked

    Example:
        >>> button = Button(
        ...     icon_path="/path/to/shutdown.png",
        ...     id="buttonPowerOff",
        ...     hint="Power Off",
        ...     command="poweroff"
        ... )
    """

    icon_path: str  # path to png icon
    id: str  # identification for css
    hint: str  # tooltip hint
    command: str  # command to run when clicked


class AppConfig(BaseConfig):
    """
    Main application configuration containing all button definitions.

    This class manages the overall application configuration loaded from YAML files.
    It uses confz for automatic YAML parsing and validation.

    Attributes:
        CONFIG_SOURCES: FileSource configuration pointing to the YAML config file
        buttons (List[Button]): List of Button objects defining power menu options

    Class Attributes:
        CONFIG_SOURCES: Default configuration source pointing to ~/.config/hyprpwmenu/config.yaml

    Example:
        >>> config = AppConfig()
        >>> print(len(config.buttons))  # Number of configured buttons
        >>> print(config.buttons[0].hint)  # First button's tooltip text

    Note:
        The CONFIG_SOURCES class attribute can be modified before instantiation
        to load configuration from a different file location.
    """

    CONFIG_SOURCES = FileSource(
        file=os.path.join(
            os.path.expanduser(path="~"), ".config", f"{APP_NAME}", "config.yaml"
        )
    )
    buttons: List[Button]


if __name__ == "__main__":
    pass
