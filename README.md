# HyprPwMenu

A modern and customizable power menu for Hyprland compositor.

## Overview

HyprPwMenu provides a sleek graphical interface for system operations like shutdown, reboot, and logoff in Hyprland Wayland compositor environments. Built with Python and PyQt6, it offers extensive customization through configuration files and CSS styling.

## Installation

### Dependencies

- Python 3.13+
- PyQt6
- click
- Font Awesome 6 (for icons)

### Installing with pip

```bash
pip install hyprpwmenu
```

### Installing from source

```bash
git clone https://github.com/your-username/hyprpwmenu.git # Replace with actual repo URL if available
cd hyprpwmenu
uv venv
source .venv/bin/activate
uv pip install -e .
```

## Usage

```bash
hyprpwmenu [OPTIONS]
```

### Command Line Options

Based on the `click.py` file, the following command-line options are available:

| Option           | Argument | Description                                   | Default Value                      |
| ---------------- | -------- | --------------------------------------------- | ---------------------------------- |
| `-c`, `--config` | `FILE`   | Specifies the path to the `config.yaml` file. | `~/.config/hyprpwmenu/config.yaml` |
| `-s`, `--style`  | `FILE`   | Specifies the path to the `style.css` file.   | `~/.config/hyprpwmenu/style.css`   |
| `-h`, `--help`   |          | Show the help message and exit.               | N/A                                |

If the specified configuration or style files don't exist at the provided paths (or the default paths), HyprPwMenu will attempt to create default versions.

## Configuration (`config.yaml`)

HyprPwMenu uses a YAML configuration file (typically `~/.config/hyprpwmenu/config.yaml`) to define its behavior and the specifics of the power actions.

_(Note: The exact structure of `config.yaml` is defined within the application's config handling logic, which was not provided. However, a typical configuration might include the following parameters):_

```yaml
# Example config.yaml structure
buttons:
  shutdown:
    command: "systemctl poweroff" # Command to execute for shutdown
    icon: "" # Font Awesome 6 icon code (e.g., power-off)
    label: "Shutdown" # Text label for the button
    keybind: "s" # Optional keyboard shortcut within the app
  reboot:
    command: "systemctl reboot"
    icon: "" # e.g., redo
    label: "Reboot"
    keybind: "r"
  logoff:
    command: "hyprctl dispatch exit" # Command for logging out of Hyprland
    icon: "" # e.g., sign-out-alt
    label: "Log Out"
    keybind: "l"
  # Add other buttons like sleep, lock screen etc. as needed
  # lock:
  #   command: "your-lock-command"
  #   icon: "" # e.g., lock
  #   label: "Lock"
  #   keybind: "k"

window:
  position: "center" # Window position (e.g., center, top-right, etc. - depends on implementation)
  width: 450 # Window width in pixels
  height: 200 # Window height in pixels
  opacity: 0.95 # Window opacity (0.0 to 1.0)
  layout: "horizontal" # Button layout (e.g., horizontal, vertical)
  spacing: 20 # Spacing between buttons

keybindings: # Global keybindings within the app
  exit: "Escape" # Key to close the power menu window

# Other potential options:
# - Font settings
# - Margins
# - Corner radius (if not handled by CSS)
```

Please refer to the default generated `config.yaml` or the application's source code for the definitive structure and available options.

## Styling (`style.css`)

The visual appearance of HyprPwMenu is controlled via a CSS file (default: `~/.config/hyprpwmenu/style.css`). The provided `assets/style.css` defines the default look and feel.

Key customizable elements via CSS include:

- **`QWidget`**: Styles the main application window background.
  - Default: Dark grey (`#121212`).
- **`QToolButton`**: Base style for all action buttons (Shutdown, Reboot, Logoff).
  - Default: Transparent background, no initial border, rounded corners (`15px`), fixed size (`100x100px`), padding (`15px`).
- **`QToolButton#<name>Button`**: Specific styling for individual buttons (e.g., `QToolButton#shutdownButton`).
  - Default: Sets the primary color for the button's text and icon.
- **`QToolButton QLabel#icon<name>Button`**: Styles the icon within a specific button.
  - Default: Uses Font Awesome 6 Free font, large size (`84px`), specific color matching the button's theme.
- **`QToolButton QLabel#text<name>Button`**: Styles the text label within a specific button.
  - Default: Arial font, `22px` size, specific color matching the button's theme.
- **`QToolButton#<name>Button:focus`**: Styles applied when a button receives focus (e.g., via keyboard navigation).
  - Default: Adds a `2px` solid border using the button's specific color.
- **`#app_info_label`**: Styles the label displaying the application name and version.
  - Default: Greenish color (`#81E7AF`), `14pt` size, padding.

Default Theme Colors:

- Shutdown: Purple (`#C68EFD`)
- Reboot: Teal (`#48A6A7`)
- Logoff: Green (`#A0C878`)

You can modify the default `style.css` or provide your own using the `-s` command-line option to completely change the appearance.

## Integration with Hyprland

To launch HyprPwMenu using a keybinding in Hyprland, add a line similar to the following to your `hyprland.conf`:

```
# Example: Bind Super + X to launch hyprpwmenu
bind = SUPER, X, exec, hyprpwmenu
```

Adjust the keybinding (`SUPER, X`) as needed.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests to the project repository.

_(Please add the actual repository link here if available)_

## License

This project is likely licensed under an open-source license. Please include a `LICENSE` file in the repository. If none is present, assume it is proprietary unless otherwise stated.
_(Consider adding a specific license, e.g., MIT License)_
