from djitellopy import Tello
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Header, Footer, Label
from textual.binding import Binding
from textual import events

from helper import show_frames, enter_recon_path
from base_widgets import ModeChoice
from screens import QuitScreen, ManualModeScreen, StateScreen, HelpScreen


class ReconPath(ModeChoice):
    TELLO: Tello = None

    BUTTON_NAME = "Enter Recon Path"
    DESCRIPTION = "Phase 1 Recon path"

    def __init__(self, tello: Tello, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TELLO = tello

    def what_to_do_on_button_pressed(self) -> None:
        enter_recon_path(self.TELLO)

    # TODO: implement stop_action method
    def stop_action(self) -> None:
        pass


class TelloGUI(App):
    """Textual app to manage tello drones"""

    CSS_PATH = "style.tcss"
    BINDINGS = [
        Binding(key="q", action="request_quit", description="Quit the app"),
        Binding(key="m", action="request_manual", description="Enter Manual Mode"),
        Binding(key="s", action="request_state", description="Show the state of Tello"),
        Binding(key="d", action="toggle_dark", description="Toggle dark mode"),
    ]

    TELLO: Tello = None

    def __init__(self, tello: Tello, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TELLO = tello

    def show_frames(self):
        show_frames(self.TELLO)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with VerticalScroll():
            yield ReconPath(self.TELLO)

    async def on_mount(self) -> None:
        self.sub_title = "by Nobu :)"
        self.set_interval(0.3, self.show_frames)

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode"""
        self.dark = not self.dark

    def _check_quit(self, quit: bool) -> None:
        if quit:
            self.exit()

    async def action_request_quit(self) -> None:
        self.push_screen(QuitScreen(), self._check_quit)

    async def action_request_manual(self) -> None:
        self.push_screen(ManualModeScreen(self.TELLO, self))

    async def action_request_state(self) -> None:
        self.push_screen(StateScreen(self.TELLO))

    def push_help_screen(self) -> None:
        self.push_screen(HelpScreen())


if __name__ == "__main__":
    tello = Tello()
    tello.connect()
    tello.streamon()

    app = TelloGUI(tello)

    # disable Tello logger
    Tello.LOGGER.disabled = True

    try:
        app.run()
    finally:
        tello.end()
