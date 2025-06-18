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

import sys
from rich.table import Table
from hyprpwmenu.util import cl, fileExists, showError, copyAssetFile
from hyprpwmenu.window import Window
from hyprpwmenu.constants import (
    APP_NAME,
    APP_VERSION,
    DEFAULT_CONFIG_FILE,
    DEFAULT_STYLE_FILE,
    DEFAULT_CONFIG_DIR,
)


def cli() -> None:
    """
    Main CLI command function for HyprPwMenu application.
    """
    cl.print(
        f"[bold cyan]{APP_NAME}[/bold cyan] [magenta]v[/magenta][green]{APP_VERSION}[/green]\n"
    )

    cl.print("Configuration Status...")
    # Criação da tabela
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Item", justify="right")
    table.add_column("Path")
    table.add_column("Status", justify="center")

    configFileOk = fileExists(file=DEFAULT_CONFIG_FILE)
    styleFileOk = fileExists(file=DEFAULT_STYLE_FILE)
    if not configFileOk:
        showError(f"{DEFAULT_CONFIG_FILE} does not exist. Creating...")
        copyAssetFile(destination=DEFAULT_CONFIG_DIR, asset="config.yaml")
        copyAssetFile(destination=DEFAULT_CONFIG_DIR, asset="logoff.png")
        copyAssetFile(destination=DEFAULT_CONFIG_DIR, asset="reboot.png")
        copyAssetFile(destination=DEFAULT_CONFIG_DIR, asset="shutdown.png")
        configFileOk = True  # Update status after creation

    if not styleFileOk:
        showError(f"{DEFAULT_STYLE_FILE} does not exist. Creating...")
        copyAssetFile(destination=DEFAULT_CONFIG_DIR, asset="style.css")
        styleFileOk = True  # Update status after creation

    table.add_row(
        "Config",
        f"[yellow]{DEFAULT_CONFIG_FILE}[/yellow]",
        f"{'[bold green]Passed[/bold green]' if configFileOk else '[bold red]Fail[/bold red]'}",
    )
    table.add_row(
        "Style",
        f"[yellow]{DEFAULT_STYLE_FILE}[/yellow]",
        f"{'[bold green]Passed[/bold green]' if styleFileOk else '[bold red]Fail[/bold red]'}",
    )

    cl.print(table)

    try:
        cl.print("Starting GUI...")
        window = Window()
        window.run()
    except Exception as e:
        showError(f"Error: {e}")
        sys.exit(1)
