"""
Utility Functions Module for HyprPwMenu

This module provides utility functions for logging, file operations, and command execution.
It uses the Rich library for enhanced console output with colors and formatting.

Functions:
    printLog: Log message with timestamp using Rich console
    printLine: Print a decorative line separator
    showStatus: Display status message with formatted preamble
    showError: Display error message with red formatting
    fileExists: Check if a file exists at the given path
    configDirExists: Check if a configuration directory exists
    executeCommand: Execute shell command and return exit code with output

Dependencies:
    - os: File system operations
    - subprocess: Process execution for shell commands
    - rich.console: Enhanced console output with colors and formatting

Global Variables:
    cl (Console): Rich console instance configured with timestamp logging
"""

import os
import subprocess
from rich.console import Console
from hyprpwmenu.constants import SPACES_DEFAULT
from hyprpwmenu.constants import APP_NAME
from typing import Tuple
import importlib.resources
import shutil


#: Rich console instance for enhanced output with timestamp logging
cl = Console(log_time_format="[%Y-%m-%d %H:%M:%S]")
# Força o Rich a não omitir timestamps repetidos
cl._log_render.omit_repeated_times = False


def printLog(message: str) -> None:
    """
    Log a message with timestamp using Rich console.

    Args:
        message: The message to be logged with timestamp

    Returns:
        None: Outputs the message to console with timestamp

    Example:
        >>> printLog("Application starting...")
        [2024-01-01 10:30:00] Application starting...
    """
    cl.log(message)


def printLine() -> None:
    """
    Print a decorative line separator to the console.

    Outputs a cyan-colored line consisting of 80 equal signs for visual separation
    in console output.

    Returns:
        None: Outputs decorative line to console

    Example:
        >>> printLine()
        ================================================================================
    """
    cl.print("[cyan]=[/cyan]" * 80)


def showStatus(preamble: str, message: str) -> None:
    """
    Display a status message with formatted preamble.

    Args:
        preamble: Status category or label (shown in yellow)
        message: The actual status message content

    Returns:
        None: Outputs formatted status message to console

    Example:
        >>> showStatus("CONFIG", "Loading configuration file...")
        CONFIG         : Loading configuration file...
    """
    cl.print(f"[bold yellow]{preamble:<{SPACES_DEFAULT}}[/bold yellow]: {message}")


def showError(message: str) -> None:
    """
    Display an error message with red formatting.

    Args:
        message: The error message to display

    Returns:
        None: Outputs formatted error message to console

    Example:
        >>> showError("Failed to load configuration")
        ERROR          : Failed to load configuration
    """
    error = "ERROR"
    cl.print(f"[bold red]{error:<{SPACES_DEFAULT}}[/bold red]: {message}")


def fileExists(file: str) -> bool:
    """
    Check if a file exists at the given path.

    Args:
        file: Absolute or relative path to the file

    Returns:
        bool: True if file exists, False otherwise

    Example:
        >>> fileExists("/home/user/config.yaml")
        True
        >>> fileExists("/nonexistent/file.txt")
        False
    """
    if os.path.isfile(file):
        return True
    else:
        return False


def configDirExists(configDir: str) -> bool:
    """
    Check if a configuration directory exists.

    Args:
        configDir: Path to the directory to check

    Returns:
        bool: True if directory exists, False otherwise

    Example:
        >>> configDirExists("/home/user/.config/hyprpwmenu")
        True
        >>> configDirExists("/nonexistent/directory")
        False
    """
    if os.path.isdir(configDir):
        return True
    else:
        return False


def executeCommand(command: str) -> Tuple[int, str, str]:
    """
    Execute a shell command and return its exit code, stdout, and stderr.

    This function runs the specified command in a shell subprocess and captures
    all output streams. It's commonly used for executing system commands like
    poweroff, reboot, or Hyprland control commands.

    Args:
        command: The shell command to execute as a string

    Returns:
        Tuple[int, str, str]: A tuple containing:
            - Exit code (0 for success, non-zero for failure)
            - Standard output as string
            - Standard error as string

    Example:
        >>> code, stdout, stderr = executeCommand("echo 'Hello World'")
        >>> print(f"Exit code: {code}, Output: {stdout.strip()}")
        Exit code: 0, Output: Hello World

        >>> code, stdout, stderr = executeCommand("poweroff")
        >>> # System will shutdown if user has permissions
    """
    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    stdout, stderr = process.communicate()
    return process.returncode, stdout, stderr


def copyAssetFile(destination: str, asset: str) -> None:
    destination = os.path.expanduser(destination)
    if not os.path.exists(destination):
        os.makedirs(destination)
    source = importlib.resources.files(APP_NAME).joinpath(f"assets/{asset}")
    shutil.copy2(str(source), destination)
