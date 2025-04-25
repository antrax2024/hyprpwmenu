import os


def main() -> None:
    from .click import cli

    try:
        del os.environ["QT_STYLE_OVERRIDE"]
    except KeyError:
        print("QT_STYLE_OVERRIDE not set, continuing...")

    cli()
