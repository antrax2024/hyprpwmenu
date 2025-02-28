import flet as ft
from config import configCheckAndLoad


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
    config = configCheckAndLoad()
    ft.app(target=main)
