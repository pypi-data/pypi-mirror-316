from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Label
from textual.containers import Container, Horizontal


class QuitScreen(ModalScreen[bool]):
    """Screen with a dialog to quit."""

    def compose(self) -> ComposeResult:
        yield Container(Label("Are you sure you want to quit?", classes="center"))
        with Horizontal(classes="center"):
            yield Button("Quit", variant="error", id="quit")
            yield Button("Cancel", variant="primary", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
            self.dismiss(True)
        else:
            self.dismiss(False)
