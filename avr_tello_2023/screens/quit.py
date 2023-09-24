from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Grid
from textual.widgets import Label, Button

class QuitScreen(Screen):
    CSS = """Button {
       width: 100%;
    }"""

    def compose(self) -> ComposeResult:
        yield Grid(
            Label('Are you sure you want to quit?', id='question'),
            Button('Quit', variant='error', id='quit'),
            Button('Cancel', variant='primary', id='cancel'),
            id='dialog',
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'quit':
            self.app.exit()
        else:
            self.app.pop_screen()
