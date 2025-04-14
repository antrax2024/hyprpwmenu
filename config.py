import os
from confz import BaseConfig, FileSource


DEBUG = True

if DEBUG:
    HOME_DIR = os.path.expanduser("~")
    CONFIG_DIR = os.path.join(HOME_DIR, ".config", "power-menu")
else:
    CONFIG_DIR = "./"


class AppConfig(BaseConfig):
    CONFIG_SOURCES = FileSource(file=os.path.join(CONFIG_DIR, "config.yaml"))
    buttonForegroundColor: str
    buttonBackgroundColor: str
    buttonHoverColor: str
    buttonFocusColor: str
    buttonBorderColor: str
    buttonBorderHoverColor: str
    buttonBorderFocusColor: str


if __name__ == "__main__":
    config = AppConfig()
    print(config)
