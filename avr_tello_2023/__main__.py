from djitellopy import Tello
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Header, Footer, Static, Button
from textual import events

from helper import show_frames, start_threads
from base_widgets import ModeChoice

class ReconPath(ModeChoice): 
    BUTTON_NAME = 'Recon Path'
    # TODO: add DESCRIPTION

class GetColor(ModeChoice):
    BUTTON_NAME = 'Get Color'
    # TODO: add DESCRIPTION

class ManualMode(ModeChoice):
    BUTTON_NAME = 'Manual Mode'
    # TODO: add DESCRIPTION
    # TODO: override on_button_pressed method

class TelloGUI(App):
    """ Textual app to manage tello drones """

    CSS_PATH = './style.tcss'
    BINDINGS = [('d', 'toggle_dark', 'Toggle dark mode')]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield ScrollableContainer(ManualMode(), ReconPath(), GetColor())

    def action_toggle_dark(self) -> None:
        """ An action to toggle dark mode """
        self.dark = not self.dark


if __name__ == '__main__':
    # tello = Tello()
    app = TelloGUI()
    
    # start_threads(tello, app)

    app.run()
