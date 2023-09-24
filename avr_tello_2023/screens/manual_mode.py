from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.containers import Horizontal, Vertical, Container
from textual.binding import Binding
from textual.widgets import Label, Button
from djitellopy import Tello

from typing import Callable

class ManualModeScreen(ModalScreen):
    TELLO: Tello = None
    DISTANCE = 50
    ROTATION = 30

    BINDINGS = [
            Binding(key='q', action='request_quit_manual', description='Quit Manual Mode'),
            Binding(key='w', action='move_forward', description="Moves the Tello drone forward"),
            Binding(key='a', action='move_left', description="Moves the Tello drone left"),
            Binding(key='d', action='move_right', description="Moves the Tello drone right"),
            Binding(key='s', action='move_backward', description="Moves the Tello drone backward"),
            Binding(key='r', action='rotate_ccw', description='Rotates the Tello drone counter clockwise'),
            Binding(key='e', action='rotate_cw', description='Rotates the Tello drone clockwise'),
            Binding(key='f', action='move_up', description='Moves the Tello drone upward'),
            Binding(key='c', action='move_down', description='Moves the Tello drone downward'),
            Binding(key='l', action='land', description='Lands the Tello drone'),
    ]

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

    def action_move_forward(self) -> None:
        self.TELLO.move_forward(self.DISTANCE)

    def action_move_backward(self) -> None:
        self.TELLO.move_back(self.DISTANCE)
    
    def action_move_left(self) -> None:
        self.TELLO.move_left(self.DISTANCE)
    
    def action_move_right(self) -> None:
        self.TELLO.move_right(self.DISTANCE)

    def action_land(self) -> None:
        self.TELLO.land()

    def action_rotate_cw(self) -> None:
        self.TELLO.rotate_clockwise(self.ROTATION)
    
    def action_rotate_ccw(self) -> None:
        self.TELLO.rotate_counter_clockwise(self.ROTATION)

    def action_move_up(self) -> None:
        self.TELLO.move_up(self.DISTANCE)
    
    def action_move_down(self) -> None:
        self.TELLO.move_down(self.DISTANCE)
