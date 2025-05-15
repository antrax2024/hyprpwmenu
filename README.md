<!-- markdownlint-disable -->

# 🚀 hyprpwmenu

<p align="center">
  <img src="https://raw.githubusercontent.com/antrax2024/hyprpwmenu/refs/heads/main/src/hyprpwmenu/assets/banner.jpg" alt="hyprpwmenu Logo">
</p>

<div align="center">
  <span>
    <img alt="PyPI - Version" src="https://img.shields.io/pypi/v/hyprpwmenu">
    <img alt="AUR Version" src="https://img.shields.io/aur/version/hyprpwmenu">
    <img alt="Python Version from PEP 621 TOML" src="https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fantrax2024%2Fhyprpwmenu%2Frefs%2Fheads%2Fmain%2Fpyproject.toml">
    <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/antrax2024/hyprpwmenu">
    <img alt="PyPI - License" src="https://img.shields.io/pypi/l/hyprpwmenu">
</span>
</div>

A modern and customizable power menu for [Hyprland](https://hyprland.org/https:/) compositor.

## 📖 Overview

**hyprpwmenu** provides a sleek graphical interface for system operations (_shutdown, reboot, and logoff_) in [Hyprland](https://hyprland.org/https:/) Wayland compositor. Built with Python and PyQt6, it offers extensive customization through configuration files and CSS styling.

## Installation

### Important

Before continuing, write these rules in your Hyprland configuration file `hyprland.conf`.

```ini
# hyprpwmenu
windowrulev2 = float,class:hyprpwmenu # necessary
#windowrulev2 = fullscreen,class:hyprpwmenu # only if you want fullscreen
windowrulev2 = size 720 250,class:hyprpwmenu
```

### Install with pip

```bash
pip install hyprpwmenu
```

### Install with AUR

**hyprpwmenu** is available in [AUR](https://aur.archlinux.org/).

```bash
paru -S hyprpwmenu
# or
yay -S  hyprpwmenu
```

## 🛠️ Usage

```bash
hyprpwmenu [OPTIONS]
```

### Command Line Options

The following command-line options are available:

| Option           | Argument | Description                                  | Default Value                      |
| ---------------- | -------- | -------------------------------------------- | ---------------------------------- |
| `-c`, `--config` | `FILE`   | Specifies the path to the`config.yaml` file. | `~/.config/hyprpwmenu/config.yaml` |
| `-s`, `--style`  | `FILE`   | Specifies the path to the`style.css` file.   | `~/.config/hyprpwmenu/style.css`   |
| `-h`, `--help`   |          | Show the help message and exit.              | N/A                                |

If the specified configuration or style files don't exist at the provided paths (or the default paths), hyprpwmenu will attempt to create default versions.

## ⚙️ Configuration (`config.yaml`)

**hyprpwmenu** uses a YAML configuration file (typically `~/.config/hyprpwmenu/config.yaml`) to define its behavior and the specifics of the power actions (shutdown, reboot and logoff).

```yaml
# This file is used to configure the hyprpwmenu
# It is a YAML file, so make sure to follow the syntax rules
# You can use comments in YAML files by starting a line with '#'

# Shutdown icon and command
# The icon is unicode for a Font Awesome icon,
# you can find the list of icons here: https://fontawesome.com/icons/
shutdown:
  icon: "\uf011"
  command: "poweroff" # Command to execute when the shutdown icon is clicked

# Reboot icon and command
reboot:
  icon: "\uf2f9"
  command: "reboot" # Command to execute when the reboot icon is clicked

# Logoff icon and command
logoff:
  icon: "\uf2f5"
  command: "hyprctl dispatch exit" # Command to execute when the logout icon is clicked
```

Please refer to the default generated `config.yaml` or the application's source code for the definitive structure and available options.

## 🎨 Styling (`style.css`)

The visual appearance of hyprpwmenu is controlled via a CSS file (default: `~/.config/hyprpwmenu/style.css`).

Key customizable elements via CSS include:

- **`QWidget`**: Styles the main application window background.
  - Default: Dark grey (`#020f18`).
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

## 🔗 Integration with Hyprland

To launch hyprpwmenu using a keybinding in Hyprland, add a line similar to the following to your `hyprland.conf`:

```ini
# Example: Bind Super + X to launch hyprpwmenu
bind = SUPER, X, exec, hyprpwmenu
```

Adjust the keybinding (`SUPER, X`) as needed.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2023 HyprPwMenu Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
