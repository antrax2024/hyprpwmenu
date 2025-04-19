import os
from confz import BaseConfig, FileSource
import argparse
import subprocess


class MainWindow(BaseConfig):
    backgrounColor: str


class AppConfig(BaseConfig):
    CONFIG_SOURCES = FileSource(
        file=os.path.join(
            os.path.expanduser(path="~"), ".config", "hyprpwmenu", "config.yaml"
        )
    )
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


def getGitVersionInfo() -> str:
    # script dir
    script_dir = os.path.dirname(os.path.realpath(__file__))
    # read version.txt
    with open(os.path.join(script_dir, "version.txt"), "r") as f:
        return f.read().strip()


if __name__ == "__main__":
    printAsciiArt()
    version = getGitVersionInfo()
    print(f"hyprpwmenu - Version: {version}")
    print("-" * 30)
