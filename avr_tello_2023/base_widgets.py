from textual.app import ComposeResult, App
from textual.widgets import Static, Button, Label

from typing import List

registered_modes: List[Static] = []

def clear_registered_modes() -> None:
    for m in registered_modes:
        m.remove_class('started')

class ModeChoice(Static):
    """ All modes inherit this class """
    
    BUTTON_NAME = ''
    DESCRIPTION = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        registered_modes.append(self)

    def compose(self) -> ComposeResult:
        yield Button(f'Enter {self.BUTTON_NAME}', id='start', variant='success')
        yield Button(f'Stop {self.BUTTON_NAME}', id='stop', variant='error')
        yield Label(self.DESCRIPTION, id='description')

    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case 'start':
                clear_registered_modes()
                self.add_class('started')
            case 'stop':
                self.remove_class('started')
