import flet as ft
import os
from pathlib import Path


CONFIG_DIR: str = Path.home().joinpath(".config", "powermenu")
CONFIG_FILE: str = "config.json"


def configCheckAndLoad() -> None:

    if Path.exists(self=Path(CONFIG_DIR)):
        print("Config directory found.")
    else:
        print("Config directory not found. Creating one...")
        os.makedirs(name=CONFIG_DIR)


def main(page: ft.Page) -> None:
    page.title = "Power Menu"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.add(
        ft.Button("Shutdown"),
        ft.Button("Reboot"),
        ft.Button("Suspend"),
        ft.Button("Hibernate"),
        ft.Button("Lock"),
        ft.Button("Logout"),
    )


if __name__ == "__main__":
    configCheckAndLoad()
    ft.app(target=main)
