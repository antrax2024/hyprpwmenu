#!/usr/bin/env bash

uv run pyinstaller main.py --name pwrmenu

DST="$HOME/pwrmenu"
ICONS_DIR="$HOME/.local/share/icons/hicolor/64x64/apps"
APP_DIR="$HOME/.local/share/applications"
APP_NAME="pwrmenu"
CONFIG_DIR="$HOME/.config/pwrmenu"

# verifica se CONFIG_DIR existe
if [ -d "$CONFIG_DIR" ]; then
  mkdir -pv "$CONFIG_DIR"
fi

# verifica se DST existe
if [ -d "$DST" ]; then
  rm -rfv "$DST"
fi

# verifica se $ICONS_DIR existe
if [ ! -d "$ICONS_DIR" ]; then
  mkdir -pv "$ICONS_DIR"
fi

# verifica se $APP_DIR existe
if [ ! -d "$APP_DIR" ]; then
  mkdir -pv "$APP_DIR"
fi

# install the app
cp -rv ./dist/* "$DST"
# copy the icon
cp "./$APP_NAME.png" "$ICONS_DIR/$APP_NAME.png"

# install desktop file
cp ./$APP_NAME.desktop "$APP_DIR/$APP_NAME.desktop"

# install config file
mkdir -pv "$CONFIG_DIR"
cp ./config.yaml "$CONFIG_DIR/config.yaml"
