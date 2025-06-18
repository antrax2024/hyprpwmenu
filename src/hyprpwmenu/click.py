"""
Command Line Interface Module for HyprPwMenu

This module provides the CLI interface for the HyprPwMenu application using the Click library.
It handles command-line argument parsing, configuration file validation, and application initialization.

The module defines command-line options for specifying custom configuration and style files,
and provides automatic creation of default files when they don't exist.

Functions:
    cli: Main CLI command function that processes arguments and launches the application

Classes:
    CustomHelpCommand: Custom Click command class for formatted help output

Constants:
    CONTEXT_SETTINGS: Click context configuration for help options
"""

import os
import sys
import click
from hyprpwmenu.config import AppConfig, FileSource, createConfigFile
from hyprpwmenu.constants import (
    APP_NAME,
    APP_VERSION,
    DEFAULT_CONFIG_FILE,
    DEFAULT_STYLE_FILE,
)


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


class CustomHelpCommand(click.Command):
    """
    Custom Click command class that provides formatted help output.

    This class extends the standard Click command to include application
    name and version information in the help display.
    """

    def format_help(self, ctx: click.Context, formatter: click.HelpFormatter) -> None:
        """
        Format and display help text with app name and version.

        Args:
            ctx: Click context object containing command information
            formatter: Click help formatter for output formatting

        Returns:
            None: Outputs formatted help text
        """
        formatter.write(f"{APP_NAME} v{APP_VERSION}\n\n")
        super().format_help(ctx=ctx, formatter=formatter)


@click.command(cls=CustomHelpCommand, context_settings=CONTEXT_SETTINGS)
@click.option(
    "-c",
    "--config",
    "configFile",
    type=click.Path(exists=False, dir_okay=False),
    default=DEFAULT_CONFIG_FILE,
    help=f"Specifies the file config.yaml file (default: {DEFAULT_CONFIG_FILE})",
)
@click.option(
    "-s",
    "--style",
    "styleFile",
    type=click.Path(exists=False, dir_okay=False),
    default=DEFAULT_STYLE_FILE,
    help=f"Specifies the style css file style.cs file (default: {DEFAULT_STYLE_FILE})",
)
def cli(configFile: str, styleFile: str) -> None:
    """
    Main CLI command function for HyprPwMenu application.

    This function processes command-line arguments, validates configuration and style files,
    creates default files if they don't exist, and initializes the GTK4 application window.

    Args:
        configFile: Path to YAML configuration file (default: ~/.config/hyprpwmenu/config.yaml)
        styleFile: Path to CSS style file (default: ~/.config/hyprpwmenu/style.css)

    Returns:
        None: Launches the GUI application

    Raises:
        SystemExit: If configuration loading fails or other critical errors occur

    Side Effects:
        - Creates default configuration and style files if they don't exist
        - Launches GTK4 window interface
        - Outputs status messages to console
    """
    click.echo(message=f"{APP_NAME} v{APP_VERSION}\n")

    if styleFile:
        if not os.path.exists(path=styleFile):
            click.echo(
                message=f"Style file does not exist: {styleFile}.\nCreating a new..."
            )
            # create the directory if it does not exist
            createConfigFile(configFile=styleFile, type="style")
        else:
            click.echo(message=f"Using style from\t: {styleFile}")

    if configFile:
        # determine if file exists

        if not os.path.exists(path=configFile):
            click.echo(
                message=f"Configuration file does not exist: {configFile}.\nCreating a new..."
            )
            # create the directory if it does not exist
            createConfigFile(configFile=configFile, type="config")
        else:
            click.echo(message=f"Using config from\t: {configFile}")

    AppConfig.CONFIG_SOURCES = FileSource(file=configFile)
    try:
        appConfig = AppConfig()
        # Initialize and launch GTK4 window
        from hyprpwmenu.window import Window

        window = Window()
        window.run()
    except Exception as e:
        click.echo(message=f"Error loading config: {e}")
        sys.exit(1)
