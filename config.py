from ast import arg
import os
from confz import BaseConfig, FileSource
import argparse
import sys
import git


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
        version=f"pwrmenu - Version: {VERSION}",
        help="Show the version and exit",
    )

    # Processamento dos argumentos
    args: argparse.Namespace = parser.parse_args()

    AppConfig.CONFIG_SOURCES = FileSource(file=args.config)
    print("Using config file: ", args.config)


def getGitVersionGitPython(repoPath=".", includeDirty=True):
    """
    Generates a version string from git describe using GitPython.
    Formats it similarly to common AUR pkgver() functions (e.g., TAG.rCOMMITS.gHASH).
    Handles cases with no tags by using the commit hash.

    Args:
        repoPath (str): Path to the repository. Defaults to current directory.
        includeDirty (bool): If True, appends '.dirty' if the repo has uncommitted changes.

    Returns:
        str: The formatted version string or a fallback error string.
    """
    try:
        # Initialize Repo object
        repo = git.Repo(path=repoPath, search_parent_directories=True)

        # Check if the repository is dirty (has uncommitted changes)
        isDirty = repo.is_dirty()

        # Attempt to get version using 'git describe --long --tags'
        try:
            # --long ensures output like TAG-COMMITS-gHASH even on exact tag match (COMMITS=0)
            # --tags ensures we describe against annotated tags
            versionStringRaw = repo.git.describe("--long", "--tags")
            versionStringRaw = versionStringRaw.strip()  # Clean whitespace

            # Parse the output (e.g., v1.2.3-10-gabcdef0)
            parts = versionStringRaw.split("-")

            if len(parts) == 3 and parts[2].startswith("g"):
                tag = parts[0]
                commitCount = parts[1]
                commitHash = parts[2]  # e.g., gabcdef0

                # Remove leading 'v' from tag if present (common in AUR)
                if tag.startswith("v"):
                    tag = tag[1:]

                # Format like AUR: TAG.rCOMMIT_COUNT.gHASH
                formattedVersion = f"{tag}.r{commitCount}.{commitHash}"
            else:
                # Fallback if format is unexpected (shouldn't happen often with --long)
                formattedVersion = versionStringRaw.replace(
                    "-", "."
                )  # Basic fallback formatting

        except git.GitCommandError as describeError:
            # This error often happens if there are no tags in the repository
            print(
                f"Info: 'git describe --tags' failed (likely no tags found): {describeError}"
            )
            # Fallback: Use the latest commit hash directly
            commitHash = repo.head.object.hexsha
            shortHash = repo.git.rev_parse(
                commitHash, short=7
            )  # Get short hash like describe
            # Format like AUR for commits with no base tag: 0.0.r0.gHASH
            formattedVersion = f"0.0.r0.g{shortHash}"
            print(
                f"Info: Falling back to version based on commit hash: {formattedVersion}"
            )

        # Append dirty marker if applicable
        if includeDirty and isDirty:
            formattedVersion += ".dirty"

        return formattedVersion

    except git.InvalidGitRepositoryError:
        print(f"Error: Path '{repoPath}' is not a valid git repository.")
        return "0.0.0.nogit"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "0.0.0.error"


if __name__ == "__main__":
    # Ensure you run this script from within a directory that is part of a Git repository
    # Or provide the path to the repository: getGitVersionGitPython(repoPath='/path/to/your/repo')

    print(
        "Attempting to generate version string from current directory's git repository..."
    )
    version = getGitVersionGitPython()
    print("-" * 30)
    print(f"Generated Version (GitPython): {version}")
    print("-" * 30)


if __name__ == "__main__":
    # passArgs()
    print(
        "Attempting to generate version string from current directory's git repository..."
    )
    version = getGitVersionGitPython()
    print("-" * 30)
    print(f"Generated Version (GitPython): {version}")
    print("-" * 30)
