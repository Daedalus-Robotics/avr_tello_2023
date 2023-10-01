from textual.app import ComposeResult, App
from textual.screen import ModalScreen
from textual.containers import Vertical
from textual.widgets import Label

from constants import MANUAL_MODE_COMMANDS

class HelpScreen(ModalScreen):
    BINDINGS = [('q', 'request_quit')]

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label('Enter "q" to quit', id='quitLabel'),
            *[Label(f'{m[0]}: {m[2]}') for m in MANUAL_MODE_COMMANDS]
        )

    def action_request_quit(self) -> None:
        self.dismiss()
