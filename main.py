import flet as ft
from config import configCheckAndLoad


def main(page: ft.Page) -> None:
    page.title = "Power Menu"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    shutdownButton = ft.IconButton(
        icon=ft.Icons.POWER_SETTINGS_NEW,
        icon_color="blue400",
        icon_size=80,
        tooltip="Shutdown the System",
        autofocus=True,
    )
    rebootButton = ft.IconButton(
        icon=ft.Icons.REFRESH,
        icon_color="blue400",
        icon_size=80,
        tooltip="Reboot the System",
    )
    logoutButton = ft.IconButton(
        icon=ft.Icons.EXIT_TO_APP,
        icon_color="blue400",
        icon_size=80,
        tooltip="Logout the User",
    )

    page.add(
        ft.SafeArea(
            content=ft.Row(
                controls=[shutdownButton, rebootButton, logoutButton],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            expand=False,
        ),
    )


if __name__ == "__main__":
    config = configCheckAndLoad()
    print(f"shutdown-command: {config['shutdown-command']}")
    print(f"reboot-command: {config['reboot-command']}")
    print(f"logout-command: {config['logout-command']}")
    ft.app(target=main)
