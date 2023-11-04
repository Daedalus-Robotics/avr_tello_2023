from textual import events
from textual.binding import Binding
from textual.app import ComposeResult, App
from textual.screen import ModalScreen
from textual.containers import Horizontal, Vertical
from textual.widgets import Label, Button
from textual.reactive import reactive
from djitellopy import Tello

from typing import List
from time import sleep

from helper import align_tello
import helper


class ManualModeScreen(ModalScreen):
    TELLO: Tello = None

    DISTANCE = 80
    ROTATION = 80

    vals = reactive([0, 0, 0, 0])

    pressed = "pressed({}, {})"

    CAMERA_DIRECTION = "forward"

    DETECTION_T = "A"

    BINDINGS = [
        Binding(key="w", action=pressed.format(1, DISTANCE)),
        Binding(key="s", action=pressed.format(1, -DISTANCE)),
        Binding(key="a", action=pressed.format(0, -DISTANCE)),
        Binding(key="d", action=pressed.format(0, DISTANCE)),
        Binding(key="W", action=pressed.format(2, DISTANCE)),
        Binding(key="S", action=pressed.format(2, -DISTANCE)),
        Binding(key="A", action=pressed.format(3, -ROTATION)),
        Binding(key="D", action=pressed.format(3, ROTATION)),
        Binding(key="c", action="toggle_camara"),
        Binding(key="C", action="toggle_detection"),
        Binding(key="t", action="takeoff"),
        Binding(key="l", action="land"),
        Binding(key="h", action="help"),
        Binding(key="q", action="quit(False)"),
        Binding(key="Q", action="quit(True)"),
        Binding(key="n", action='align("A")'),
        Binding(key="N", action='align("H")'),
    ]

    def __init__(self, tello: Tello, app: App, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TELLO = tello
        self.APP = app

    def compose(self) -> ComposeResult:
        widget = Vertical(
            Label('Enter "q" to quit Manual Mode', id="quitLabel"),
            Button(
                "Forward",
                variant="primary",
                id="forwardButton",
                name="directionButtons",
            ),
            Horizontal(
                Button(
                    "Left", variant="primary", id="leftButton", name="directionButtons"
                ),
                Button(
                    "Right",
                    variant="primary",
                    id="rightButton",
                    name="directionButtons",
                ),
                id="leftRightHorizontal",
            ),
            Button(
                "Backward",
                variant="primary",
                id="backwardButton",
                name="directionButtons",
            ),
            id="manualModeScreenVertical",
        )

        yield widget

    def validate_vals(self, vals) -> List[int]:
        self.TELLO.send_rc_control(*vals)
        sleep(1 / 4)
        self.TELLO.send_rc_control(0, 0, 0, 0)
        return [0, 0, 0, 0]

    def action_takeoff(self) -> None:
        self.TELLO.takeoff()

    def action_land(self) -> None:
        self.TELLO.land()

    def action_toggle_camara(self) -> None:
        if self.CAMERA_DIRECTION == "forward":
            self.TELLO.send_command_with_return("downvision 1")
            self.CAMERA_DIRECTION = "backward"
        else:
            self.TELLO.send_command_with_return("downvision 0")
            self.CAMERA_DIRECTION = "forward"

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quitButton":
            self.dismiss()

    def action_pressed(self, val_idx: int, distance: int) -> None:
        vals = [0 for _ in range(4)]
        vals[val_idx] = distance
        self.vals = vals

    def action_quit(self, immediately: bool) -> None:
        if immediately:
            self.TELLO.emergency()
        else:
            self.dismiss()

    def action_help(self) -> None:
        self.APP.push_help_screen()

    def action_align(self, l: str) -> None:
        align_tello(self.TELLO, detection_type=l)

    def action_toggle_detection(self) -> None:
        if self.DETECTION_T == "A":
            helper.DETECTION_TYPE = "H"
            self.DETECTION_T = "H"
        else:
            helper.DETECTION_TYPE = "A"
            self.DETECTION_T = "A"
