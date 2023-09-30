from djitellopy import Tello
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Header, Footer, Label
from textual.binding import Binding
from textual import events

from helper import show_frames, start_threads
from base_widgets import ModeChoice
from screens import QuitScreen, ManualModeScreen, StateScreen

class ReconPath(ModeChoice): 
    BUTTON_NAME = 'Recon Path'
    # TODO: add DESCRIPTION
    DESCRIPTION = 'recon pathhhhhh'
    
    # TODO: implement what_to_do_on_button_pressed method

    # TODO: implement stop_action method
    def stop_action(self) -> None:
        pass


class TelloGUI(App):
    """ Textual app to manage tello drones """

    CSS_PATH = 'style.tcss'
    BINDINGS = [
            Binding(key='q', action='request_quit', description='Quit the app'),
            Binding(key='m', action='request_manual', description='Enter Manual Mode'),
            Binding(key='s', action='request_state', description='Show the state of Tello'),
            Binding(key='d', action='toggle_dark', description='Toggle dark mode'),
    ]
    
    TELLO: Tello = None

    def __init__(self, tello: Tello, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TELLO = tello

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with VerticalScroll():
            yield ReconPath()

    async def on_mount(self) -> None:
        self.sub_title = 'by Nobu :)'

    def action_toggle_dark(self) -> None:
        """ An action to toggle dark mode """
        self.dark = not self.dark
    
    def _check_quit(self, quit: bool) -> None:
        if quit:
            self.exit()

    async def action_request_quit(self) -> None:
        self.push_screen(QuitScreen(), self._check_quit)

    async def action_request_manual(self) -> None:
        self.push_screen(ManualModeScreen(self.TELLO))

    async def action_request_state(self) -> None:
        self.push_screen(StateScreen(self.TELLO))

if __name__ == '__main__':
    tello = Tello()
    tello.connect()
    
    app = TelloGUI(tello)

    # disable Tello logger
    Tello.LOGGER.disabled = True
    
    # start_threads(tello, app)
    
    try:
        app.run()
    finally:
        tello.end()
