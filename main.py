import flet as ft
from config import configCheckAndLoad
from dbus_notification import DBusNotification
import subprocess


def executeCommand(
    command: list[str],
    timeout: int = 30,
    capture_output: bool = True,
    error_verify: bool = True,
) -> subprocess.CompletedProcess:
    """
    Executa comandos Linux com segurança e controle total

    Parâmetros:
        comando (list): Lista de argumentos (ex: ["ls", "-l"])
        timeout (int): Tempo máximo de execução em segundos
        capturar_saida (bool): Captura stdout/stderr
        verificar_erro (bool): Lança exceção em códigos de erro ≠ 0

    Retorna:
        CompletedProcess: Objeto com resultados da execução
    """
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
    page.window.title_bar_hidden = config["window"]["title-bar-hidden"]
    page.title = config["window"]["title"]
    page.window.always_on_top = config["window"]["always-on-top"]
    page.window.skip_task_bar = config["window"]["skip-task-bar"]
    page.window.height = config["window"]["height"]
    page.window.center()

    def shutdownButtonClicked(e) -> None:
        print("Shutdown Button Clicked")
        sendNotification(title="Shutdown", message="System will shutdown...")
        executeCommand(command=config["shutdown-command"])
        e.page.window.destroy()

    def rebootButtonClicked(e) -> None:
        print("Reboot Button Clicked")
        sendNotification(title="Reboot", message="System will reboot...")
        executeCommand(command=config["reboot-command"])
        e.page.window.destroy()

    def logoutButtonClicked(e) -> None:
        print("Logout Button Clicked")
        sendNotification(title="Logout", message="User will be logged out...")
        executeCommand(command=config["logout-command"])
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
    config = configCheckAndLoad()
    ft.app(target=main)
