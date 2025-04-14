import os
from confz import BaseConfig, FileSource


DEBUG = True

if DEBUG:
    HOME_DIR = os.path.expanduser("~")
    CONFIG_DIR = os.path.join(HOME_DIR, ".config", "power-menu")
else:
    CONFIG_DIR = "."


class AppConfig(BaseConfig):
    CONFIG_SOURCES = FileSource(file="./config.yaml")
    colorButton: str


if __name__ == "__main__":
    config = AppConfig()
    print(config)
