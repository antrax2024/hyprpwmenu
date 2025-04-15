from ast import arg
import os
from confz import BaseConfig, FileSource
import argparse
import sys


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
    # Configuração do parser
    parser = argparse.ArgumentParser(
        description=f"pwrmenu - A Modern Power Menu for Hyprland. Version: {VERSION}.",
    )

    # Argumentos opcionais
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

    # Processamento dos argumentos
    args: argparse.Namespace = parser.parse_args()

    AppConfig.CONFIG_SOURCES = FileSource(file=args.config)
    print("Using config file: ", args.config)


if __name__ == "__main__":
    printAsciiArt()
    passArgs()
