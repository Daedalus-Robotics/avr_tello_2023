from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.containers import Horizontal, Vertical, Container
from textual.binding import Binding
from textual.widgets import Label, Button
from djitellopy import Tello

from typing import Callable

from helper import get_battery

class BatteryLabel(Label):
    TELLO: Tello = None

    def __init__(self, tello: Tello, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TELLO = tello
    
    def compose(self) -> ComposeResult:
        yield Label(get_battery(self.TELLO))

class StateScreen(ModalScreen):
    TELLO: Tello = None
    BINDINGS = [
            Binding(key='q', action='request_quit', description='Quit'),
    ]

    def __init__(self, tello: Tello, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TELLO = tello

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label('Enter "q" to quit'),
            BatteryLabel(self.TELLO),
            id='stateScreen'
        )

    def action_request_quit(self) -> None:
        self.dismiss()
