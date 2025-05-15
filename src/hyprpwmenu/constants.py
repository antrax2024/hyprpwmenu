# This is the version of the application.
import os


APP_VERSION = "0.1.18"
# This is the name of the application.
APP_NAME = "hyprpwmenu"

DEFAULT_CONFIG_FILE = os.path.join(
    os.path.expanduser(path="~"), ".config", f"{APP_NAME}", "config.yaml"
)

DEFAULT_STYLE_FILE = os.path.join(
    os.path.expanduser(path="~"), ".config", f"{APP_NAME}", "style.css"
)
