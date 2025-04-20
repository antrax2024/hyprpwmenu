import os
import sys
import click
from .config import AppConfig, FileSource, createConfigFile
from .constants import APP_NAME, APP_VERSION, DEFAULT_CONFIG_FILE, DEFAULT_STYLE_FILE
from PyQt6.QtWidgets import QApplication
from .kernel import MainWindow


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


class CustomHelpCommand(click.Command):
    def format_help(self, ctx: click.Context, formatter: click.HelpFormatter) -> None:
        """Custom help formatter that includes app name and version."""
        formatter.write(f"{APP_NAME} v{APP_VERSION}\n\n")
        super().format_help(ctx=ctx, formatter=formatter)


@click.command(cls=CustomHelpCommand, context_settings=CONTEXT_SETTINGS)
@click.option(
    "-c",
    "--config",
    "config_file",
    type=click.Path(exists=False, dir_okay=False),
    default=DEFAULT_CONFIG_FILE,
    help=f"Specifies the file config.yaml file (default: {DEFAULT_CONFIG_FILE})",
)
@click.option(
    "-s",
    "--style",
    "style_file",
    type=click.Path(exists=False, dir_okay=False),
    default=DEFAULT_STYLE_FILE,
    help=f"Specifies the style css file style.cs file (default: {DEFAULT_STYLE_FILE})",
)
def cli(config_file, style_file) -> None:
    """A modern powermenu for Hyprland."""
    click.echo(message=f"{APP_NAME} v{APP_VERSION}\n")

    if style_file:
        if not os.path.exists(path=style_file):
            click.echo(
                message=f"Style file does not exist: {style_file}.\nCreating a new..."
            )
            # create the directory if it does not exist
            createConfigFile(configFile=style_file, type="style")
        else:
            click.echo(message=f"Using style from\t: {style_file}")

    if config_file:
        # determine if file exists

        if not os.path.exists(path=config_file):
            click.echo(
                message=f"Configuration file does not exist: {config_file}.\nCreating a new..."
            )
            # create the directory if it does not exist
            createConfigFile(configFile=config_file, type="config")
        else:
            click.echo(message=f"Using config from\t: {config_file}")

    AppConfig.CONFIG_SOURCES = FileSource(file=config_file)
    try:
        appConfig = AppConfig()
        app = QApplication(sys.argv)
        window = MainWindow(appConfig=appConfig, style_file=style_file)
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        click.echo(message=f"Error loading config: {e}")
        sys.exit(1)
