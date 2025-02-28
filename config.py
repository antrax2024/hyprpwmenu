import json
from pathlib import Path


CONFIG_PATH: Path = Path.home().joinpath(".config", "powermenu", "config.json")


def save_config(config_data: dict) -> None:
    """Saves configuration data to JSON file with error handling

    Args:
        config_data: Dictionary containing configuration parameters

    Raises:
        IOError: On file write permissions issues
        JSONEncodeError: For unserializable data types
    """
    try:
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with CONFIG_PATH.open("w") as f:
            json.dump(config_data, f, indent=4, ensure_ascii=False)
    except (IOError, PermissionError) as e:
        print(f"Error saving configuration: {str(e)}")


def load_config(default: dict = None) -> dict:
    """Loads configuration from JSON file

    Args:
        default: Fallback values if file doesn't exist

    Returns:
        Dictionary with configuration values
    """
    try:
        with CONFIG_PATH.open() as f:
            return json.load(f)
    except FileNotFoundError:
        return default or {}
    except json.JSONDecodeError as e:
        print(f"Invalid JSON format: {str(e)}")
        return default or {}
    except Exception as e:
        print(f"Error loading configuration: {str(e)}")
        return default or {}


def configCheckAndLoad():
    if not CONFIG_PATH.exists():
        homeDir = Path().home()
        save_config(
            config_data={
                "window": {
                    "title": "Power Menu",
                    "title-bar-hidden": True,
                    "always-on-top": True,
                    "skip-task-bar": True,
                    "height": 120,
                },
                "icons": {
                    "size": 80,
                    "color": "blue400",
                },
                "shutdown-command": f"{homeDir}/dotfiles/bin/shutdown.sh shutdown",
                "reboot-command": f"{homeDir}/dotfiles/bin/shutdown.sh reboot",
                "logout-command": "hyprctl dispatch exit",
                "suspend-command": "systemctl suspend",
            }
        )

    return load_config(default={"version": 1.0})
