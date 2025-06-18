"""
Application Constants Module for HyprPwMenu

This module defines global constants used throughout the HyprPwMenu application.
It includes version information, application name, default file paths, and
configuration parameters.

Constants:
    APP_VERSION (str): Current version of the application
    APP_NAME (str): Application name used for configuration directories
    DEFAULT_CONFIG_FILE (str): Default path for YAML configuration file
    DEFAULT_STYLE_FILE (str): Default path for CSS style file
    SPACES_DEFAULT (int): Default spacing value for console output formatting


"""

import os

#: Current version of the HyprPwMenu application
APP_VERSION = "0.2.5"

#: Application name used for configuration directories and identification
APP_NAME = "hyprpwmenu"


# default configuration and style file paths
DEFAULT_CONFIG_DIR = os.path.join(
    os.path.expanduser(path="~"), ".config", f"{APP_NAME}"
)

#: Default path for the YAML configuration file containing button definitions
DEFAULT_CONFIG_FILE = os.path.join(DEFAULT_CONFIG_DIR, "config.yaml")

#: Default path for the CSS style file containing visual theme definitions
DEFAULT_STYLE_FILE = os.path.join(DEFAULT_CONFIG_DIR, "style.css")

#: Default spacing value used for console output formatting in utility functions
SPACES_DEFAULT = 15
