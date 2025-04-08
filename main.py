import flet as ft
from dbus_notification import DBusNotification
import subprocess


config = {
    "icons": {
        "size": 80,
        "color": "blue400",
    },
    "shutdown-command": ["sudo shutdown -h now"],
    "reboot-command": ["reboot"],
    "logout-command": ["hyprctl", "dispatch", "exit"],
}


def executeCommand(
    command: list[str],
    timeout: int = 30,
    capture_output: bool = True,
    error_verify: bool = True,
) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(
            args=command,
            check=error_verify,
            timeout=timeout,
            stdout=subprocess.PIPE if capture_output else None,
            stderr=subprocess.PIPE if capture_output else None,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Erro no comando {command[0]} (código {e.returncode})"
        ) from e
    except subprocess.TimeoutExpired:
        raise TimeoutError(f"Timeout excedido para {command[0]}")


def sendNotification(title: str, message: str) -> None:
    DBusNotification(appname="pwrmenu").send(
        title=title,
        message=message,
    )


def main(page: ft.Page) -> None:
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window.title_bar_hidden = True
    page.title = "Power Menu"

    def on_keyboard(e: ft.KeyboardEvent) -> None:
        page.update()
        if e.key == "Escape":
            page.window.destroy()

    page.on_keyboard_event = on_keyboard

    def shutdownButtonClicked(e) -> None:
        print("Shutdown Button Clicked")
        executeCommand(command="sudo shutdown -h now")
        e.page.window.destroy()

    def rebootButtonClicked(e) -> None:
        print("Reboot Button Clicked")
        executeCommand(command="sudo reboot")
        e.page.window.destroy()

    def logoutButtonClicked(e) -> None:
        print("Logout Button Clicked")
        executeCommand(command="hyprctl dispatch exit")
        e.page.window.destroy()

    shutdownButton = ft.IconButton(
        icon=ft.Icons.POWER_SETTINGS_NEW,
        icon_color=config["icons"]["color"],
        icon_size=config["icons"]["size"],
        tooltip="Shutdown the System",
        autofocus=True,
        on_click=shutdownButtonClicked,
    )
    rebootButton = ft.IconButton(
        icon=ft.Icons.REFRESH,
        icon_color=config["icons"]["color"],
        icon_size=config["icons"]["size"],
        tooltip="Reboot the System",
        on_click=rebootButtonClicked,
    )
    logoutButton = ft.IconButton(
        icon=ft.Icons.EXIT_TO_APP,
        icon_color=config["icons"]["color"],
        icon_size=config["icons"]["size"],
        tooltip="Logout the User",
        on_click=logoutButtonClicked,
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
    ft.app(target=main)
