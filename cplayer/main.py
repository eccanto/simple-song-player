"""Entry point for the Song Player Console Application.

The application provides a console-based user interface to manage and play songs, create and manage playlists,
adjust volume levels, and control song playback.

Author: Erik Ccanto
Date: 30 Jul 2023
"""

import os


os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

# pylint: disable=wrong-import-position

import logging
from pathlib import Path
from typing import Optional

import click
from pygame import mixer
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Header

from cplayer.src.elements.config import Config
from cplayer.src.pages.help import HelpPage
from cplayer.src.pages.home import HomePage


__LOGGING_FORMAT = '[%(asctime)s] [%(process)d] %(filename)s:%(lineno)d - %(levelname)s - %(message)s'
__DEFAULT_CONFIG = Path(__file__).parent.joinpath('resources/config/default.yaml')

CONFIG = Config(default_data=__DEFAULT_CONFIG)


class Application(App):
    """Class that represent the main application and inherits from the textual App class."""

    TITLE = ' Playlist'
    CSS_PATH = Path(__file__).parent.joinpath('resources/styles/application.css')
    BINDINGS = [
        Binding('q', 'quit', 'Quit', show=True),
        Binding('h', 'home', 'Home', show=True),
        Binding('i', 'info', 'Info', show=True),
    ]

    def __init__(self, path: Optional[Path], *args, **kwargs) -> None:
        """Initializes the Application object.

        :param path: The optional path of the directory songs.
        :param *args: Variable length argument list.
        :param **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)

        self.home_page = HomePage(path if path else Path('.'), change_title=self.set_title, start_hidden=False)
        self.help_page = HelpPage(change_title=self.set_title)

    def compose(self) -> ComposeResult:
        """Composes the application layout.

        :returns: The ComposeResult object representing the composed layout.
        """
        yield Header()

        yield self.home_page
        yield self.help_page

        if CONFIG.data.appearance.style.footer:
            yield Footer()

    def set_title(self, title: str) -> None:
        """Sets the title of the application window.

        :param title: The title of the application window.
        """
        self.title = title

    def action_info(self) -> None:
        """Opens the information window."""
        help_page = self.query_one(HelpPage)
        help_page.show()

        home_path = self.query_one(HomePage)
        home_path.hide()

    def action_home(self) -> None:
        """Opens the home window."""
        home_path = self.query_one(HomePage)
        home_path.show()

        help_page = self.query_one(HelpPage)
        help_page.hide()


@click.command()
@click.option('-p', '--path', help='Songs directory path.', type=click.Path(exists=True, path_type=Path))
def main(path: Optional[Path]) -> None:
    """Command line music player."""
    mixer.init()

    app = Application(path)
    app.run()


if __name__ == '__main__':
    logging.basicConfig(
        filename=Path(CONFIG.data.development.logfile).expanduser(),
        level=logging.getLevelName(CONFIG.data.development.level),
        format=__LOGGING_FORMAT,
    )

    main()  # pylint: disable=no-value-for-parameter
