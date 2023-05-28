from pathlib import Path
from typing import Callable, Coroutine

from textual.app import ComposeResult
from textual.containers import Center
from textual.widget import Widget
from textual.widgets import Input, Label

from components.hidden_widget.widget import HiddenWidget


class InputLabel(HiddenWidget):
    """An input with a label."""

    BINDINGS = [
        ('escape', 'quit', 'Quit'),
    ]

    DEFAULT_CSS = Path(__file__).parent.joinpath('styles.css').read_text()

    def __init__(
        self,
        input_label: str,
        on_enter: Callable[[], Coroutine[None, None, None]],
        on_quit: Callable[['InputLabel'], None],
        *args,
        **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)

        self.input_label = input_label
        self.on_enter = on_enter
        self.on_quit = on_quit

    def compose(self) -> ComposeResult:
        with Center():
            yield Label(self.input_label)

            input = Input()
            input.action_submit = self.on_enter

            yield input

    @property
    def value(self):
        input = self.query_one(Input)
        return input.value

    def action_quit(self):
        self.on_quit(self)

    def focus(self):
        input = self.query_one(Input)
        input.focus()

    async def action_search(self):
        await self.on_enter()

        self.visible = False
