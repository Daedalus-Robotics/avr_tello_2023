from djitellopy import Tello
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Header, Footer
from textual.binding import Binding
from textual import events

from helper import show_frames, start_threads
from base_widgets import ModeChoice

class ReconPath(ModeChoice): 
    BUTTON_NAME = 'Recon Path'
    # TODO: add DESCRIPTION
    DESCRIPTION = 'recon pathhhhhh'

class GetColor(ModeChoice):
    BUTTON_NAME = 'Get Color'
    # TODO: add DESCRIPTION
    DESCRIPTION = 'get colorrr'

class ManualMode(ModeChoice):
    BUTTON_NAME = 'Manual Mode'
    # TODO: add DESCRIPTION
    DESCRIPTION = 'manual modeeeee'

# class ManualModeScreen()

class TelloGUI(App):
    """ Textual app to manage tello drones """

    CSS_PATH = 'style.tcss'
    BINDINGS = [
            Binding(key='q', action='quit', description='Quit the app'),
            Binding(key='d', action='toggle_dark', description='Toggle dark mode'),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield ScrollableContainer(ManualMode(), ReconPath(), GetColor())

    def on_mount(self) -> None:
        self.sub_title = 'by Nobu and others'

    def action_toggle_dark(self) -> None:
        """ An action to toggle dark mode """
        self.dark = not self.dark

if __name__ == '__main__':
    # tello = Tello()
    app = TelloGUI()
    
    # start_threads(tello, app)

    app.run()
