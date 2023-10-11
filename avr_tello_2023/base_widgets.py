from textual.app import ComposeResult, App
from textual.widgets import Static, Button, Label

from typing import List, Any

registered_modes: List[Any] = []


def clear_registered_modes() -> None:
    for m in registered_modes:
        m.remove_class("started")
        m.stop_action()


class ModeChoice(Static):
    """All modes inherit this class"""

    BUTTON_NAME = ""
    DESCRIPTION = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        registered_modes.append(self)

    def compose(self) -> ComposeResult:
        yield Button(f"Enter {self.BUTTON_NAME}", id="start", variant="success")
        yield Button(f"Stop {self.BUTTON_NAME}", id="stop", variant="error")
        yield Label(self.DESCRIPTION, id="description")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "start":
                clear_registered_modes()
                self.what_to_do_on_button_pressed()
                self.add_class("started")

            case "stop":
                self.remove_class("started")

    def what_to_do_on_button_pressed(self) -> None:
        raise NotImplementedError(
            "what_to_do_on_button_pressed method must be implemented"
        )

    def stop_action(self) -> None:
        raise NotImplementedError("stop_action method must be implemented")
