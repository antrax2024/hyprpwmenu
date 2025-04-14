import os
from confz import BaseConfig, FileSource


DEBUG = True

if DEBUG:
    fileSource = FileSource(file="config.yaml")
else:
    HOME_DIR = os.path.expanduser("~")
    CONFIG_DIR = os.path.join(HOME_DIR, ".config", "power-menu")
    fileSource = FileSource(file=os.path.join(CONFIG_DIR, "./config.yaml"))


class AppConfig(BaseConfig):
    CONFIG_SOURCES = fileSource
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


if __name__ == "__main__":
    config = AppConfig()
    print(config)
