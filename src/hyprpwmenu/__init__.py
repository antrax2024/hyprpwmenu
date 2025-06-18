"""
HyprPwMenu Package

A modern and customizable power menu for Hyprland Wayland compositor.

This package provides a graphical interface for system operations (shutdown, reboot, logoff)
built with Python and GTK4. It offers extensive customization through YAML configuration
files and CSS styling.

Features:
    - Modern GTK4-based interface using gtk4-layer-shell
    - Customizable buttons through YAML configuration
    - CSS styling support for visual customization
    - Keyboard navigation with arrow keys
    - Mouse interaction support
    - Integration with Hyprland compositor

Example:
    Basic usage from command line:
        $ hyprpwmenu

    With custom configuration:
        $ hyprpwmenu --config ~/my-config.yaml --style ~/my-style.css

Attributes:
    APP_NAME (str): Application name constant
    APP_VERSION (str): Current version of the application
    DEFAULT_CONFIG_FILE (str): Default path for configuration file
    DEFAULT_STYLE_FILE (str): Default path for CSS style file
"""

# filepath: /home/antrax/Dev/hyprpwmenu/src/hyprpwmenu/__init__.py


def main() -> None:
    """
    Main entry point for the HyprPwMenu application.

    This function imports and executes the CLI interface from the click module.
    It serves as the primary entry point when the package is run as a script
    or installed as a console script.

    The function initializes the command-line interface which handles:
    - Configuration file validation and creation
    - Style file validation and creation
    - Application configuration loading
    - GTK4 window initialization and display

    Returns:
        None: This function does not return a value

    Raises:
        ImportError: If the click module or its dependencies cannot be imported
        SystemExit: If configuration loading fails or other critical errors occur

    Example:
        >>> from hyprpwmenu import main
        >>> main()  # Launches the power menu GUI
    """
    from .click import cli

    cli()
