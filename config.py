import os
from confz import BaseConfig, FileSource
import argparse
import subprocess


VERSION = "0.1.2"


class MainWindow(BaseConfig):
    backgrounColor: str


class AppConfig(BaseConfig):
    CONFIG_SOURCES = FileSource(file="config.yaml")
    iconColor: str
    iconColorActive: str
    iconSizeW: int
    iconSizeH: int
    shutdownIcon: str
    rebootIcon: str
    logoffIcon: str
    shutdownCommand: str
    rebootCommand: str
    logoffCommand: str
    MainWindow: MainWindow


def printAsciiArt() -> None:
    asciiArt = r"""
_ ____      ___ __ _ __ ___   ___ _ __  _   _ 
| '_ \ \ /\ / / '__| '_ ` _ \ / _ \ '_ \| | | |
| |_) \ V  V /| |  | | | | | |  __/ | | | |_| |
| .__/ \_/\_/ |_|  |_| |_| |_|\___|_| |_|\__,_|
|_|    
    """
    print(asciiArt)


def passArgs() -> None:
    printAsciiArt()
    # Configuração do parser
    parser = argparse.ArgumentParser(
        description=f"pwrmenu - A Modern Power Menu for Hyprland. Version: {VERSION}.",
    )

    # Argumentos
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        default=os.path.join(
            os.path.expanduser(path="~"), ".config", "pwrmenu", "config.yaml"
        ),
        required=False,
        help="Path to the config file (config.yaml)",
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"pwrmenu - Version: {getGitVersionInfo()}",
        help="Show the version and exit",
    )

    # Processamento dos argumentos
    args: argparse.Namespace = parser.parse_args()

    AppConfig.CONFIG_SOURCES = FileSource(file=args.config)
    print("Using config file: ", args.config)


def getGitVersionInfo():
    """
    Retrieves git commit count and short hash, mimicking the shell script:
    printf "%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"

    Ensures commands are run within a git repository.

    Returns:
        str: A string formatted as "commit_count.short_hash",
        or None if not in a git repository or if git commands fail.
    """
    try:
        # Verify it's a git repository first to avoid unnecessary errors later
        # Using check=True will raise CalledProcessError if the command fails (e.g., not a git repo)
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,  # Raise exception on non-zero exit code
            capture_output=True,  # Capture stdout and stderr
            text=True,  # Decode output as text using default encoding
            encoding="utf-8",  # Specify UTF-8 encoding
        )

        # Get commit count using check_output
        commitCountBytes = subprocess.check_output(
            ["git", "rev-list", "--count", "HEAD"],
            stderr=subprocess.PIPE,  # Redirect stderr to avoid printing it
            encoding="utf-8",  # Specify UTF-8 encoding
        )
        commitCount = (
            commitCountBytes.strip()
        )  # Remove leading/trailing whitespace (like newline)

        # Get short commit hash using check_output
        shortHashBytes = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            stderr=subprocess.PIPE,  # Redirect stderr
            encoding="utf-8",  # Specify UTF-8 encoding
        )
        shortHash = shortHashBytes.strip()  # Remove leading/trailing whitespace

        # Format the output string as "count.hash"
        versionInfo = f"{commitCount}.{shortHash}"
        return versionInfo

    except FileNotFoundError:
        # Handle error if git is not installed or not in PATH
        print(
            "Error: 'git' command not found. Make sure Git is installed and in your PATH."
        )
        return None
    except subprocess.CalledProcessError as e:
        # Handle errors if git commands fail
        # Common reason: not running inside a git repository
        # Check stderr to provide a more specific error message
        error_message = (
            e.stderr.decode("utf-8").strip()
            if hasattr(e, "stderr") and e.stderr
            else str(e)
        )
        if "not a git repository" in error_message.lower():
            print(f"Error: Not inside a git repository.")  # Simplified message
        else:
            # General error message for other git command failures
            print(f"Error executing git command: {e}. Stderr: {error_message}")
        return None
    except Exception as e:
        # Catch any other unexpected errors during execution
        print(f"An unexpected error occurred: {e}")
        return None


if __name__ == "__main__":
    passArgs()
    # print(
    #     "Attempting to generate version string from current directory's git repository..."
    # )
    # version = getGitVersionInfo()
    # print("-" * 30)
    # print(f"Generated Version (GitPython): {version}")
    # print("-" * 30)
