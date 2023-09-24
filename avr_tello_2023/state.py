from textual.app import ComposeResult
from textual.widgets import Label
from djitellopy import Tello

from threading import Thread
from time import sleep

from helper import get_battery

class Battery(Label):
    TELLO: Tello = None
    
    def __init__(self, tello: Tello, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TELLO = tello
        # starts updating the battery label
        Thread(target=self.update_battery_label, daemon=True).start()

    def update_battery_label(self) -> None:
        while True:
            new_battery = get_battery(self.TELLO)
            self.update(new_battery)
            sleep(1 / 3)

class TelloState(Label):
    TELLO: Tello = None

    def __init__(self, tello: Tello, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TELLO = tello

    def compose(self) -> ComposeResult:
        # TODO: add other states needed here!
        yield Battery(self.TELLO, get_battery(self.TELLO))
