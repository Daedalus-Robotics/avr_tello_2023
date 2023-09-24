from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.containers import Horizontal, Vertical, Container
from textual.binding import Binding
from textual.widgets import Label, Button
from djitellopy import Tello

class ManualModeScreen(ModalScreen):
    TELLO = None

    BINDINGS = [Binding(key='q', action='request_quit_manual', description='Quit Manual Mode')]

    def __init__(self, tello: Tello, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TELLO = tello

    def compose(self) -> ComposeResult:
        widget = Vertical(
            Label('Enter "q" to quit Manual Mode', id='quitLabel'),
            Button('Forward', variant='primary', id='forwardButton', name='directionButtons'),
            Horizontal(
                Button('Left', variant='primary', id='leftButton', name='directionButtons'),
                Button('Right', variant='primary', id='rightButton', name='directionButtons'),
                id='leftRightHorizontal'
            ),
            Button('Backward', variant='primary', id='backwardButton', name='directionButtons'),
            
            id='manualModeScreenVertical'
        )
        
        yield widget

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'quitButton':
            self.dismiss()

    def action_request_quit_manual(self) -> None:
        self.dismiss()
