from textual.app import ComposeResult
from textual.widgets import Static, Button

class ModeChoice(Static):
    """ All modes inherit this class """
    
    BUTTON_NAME = ''
    DESCRIPTION = ''

    def compose(self) -> ComposeResult:
        yield Button(f'Enter {self.BUTTON_NAME}', id='start', variant='success')
        yield Button(f'Stop {self.BUTTON_NAME}', id='stop', variant='error')
        yield Static(self.DESCRIPTION, id='description')

    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case 'start':
                self.add_class('started')
            case 'stop':
                self.remove_class('started')
