from textual.app import ComposeResult, App
from textual.screen import ModalScreen
from textual.containers import Horizontal, Vertical
from textual.binding import Binding
from textual.widgets import Label, Button
from textual.reactive import reactive
from djitellopy import Tello

from time import sleep
from typing import List

from constants import MANUAL_MODE_COMMANDS

class ManualModeScreen(ModalScreen):
    TELLO: Tello = None
    
    DISTANCE = 50
    ROTATION = 30

    BINDINGS = \
        [Binding(key=m[0], action=m[1], description=m[2]) for m in MANUAL_MODE_COMMANDS] + \
        [Binding(key='h', action='request_help', description='Show Help screen')]

    vals = reactive([0, 0, 0, 0])

    def __init__(self, tello: Tello, app: App, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TELLO = tello
        self.APP = app

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

    def validate_vals(self, vals) -> List[int]:
        self.TELLO.send_rc_control(*vals)
        return [0, 0, 0, 0]

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'quitButton':
            self.dismiss()

    def action_request_quit_manual(self) -> None:
        self.dismiss()

    def action_move_forward(self) -> None:
        self.vals = [self.vals[0], self.DISTANCE, self.vals[2], self.vals[3]]

    def action_move_backward(self) -> None:
        self.vals = [self.vals[0], -self.DISTANCE, self.vals[2], self.vals[3]]

    def action_move_left(self) -> None:
        self.vals = [-self.DISTANCE, self.vals[1], self.vals[2], self.vals[3]]

    def action_move_right(self) -> None:
        self.vals = [self.DISTANCE, self.vals[1], self.vals[2], self.vals[3]]

    def action_land(self) -> None:
        self.TELLO.land()

    def action_rotate_cw(self) -> None:
        self.vals = [self.vals[0], self.vals[1], self.vals[2], self.ROTATION]

    def action_rotate_ccw(self) -> None:
        self.vals = [self.vals[0], self.vals[1], self.vals[2], -self.ROTATION]

    def action_move_up(self) -> None:
        self.vals = [self.vals[0], self.vals[1], self.DISTANCE, self.vals[3]]

    def action_move_down(self) -> None:
        self.vals = [self.vals[0], self.vals[1], -self.DISTANCE, self.vals[3]]

    def action_takeoff(self) -> None:
        self.TELLO.takeoff()

    def action_request_help(self) -> None:
        self.APP.push_help_screen()
