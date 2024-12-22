from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Button, Input, Label
from textual.screen import ModalScreen

import os


class LogExportPath(ModalScreen):
    "A logs export path popup modal."

    def __init__(self, log_path: str, logs: list, detailed: bool) -> None:
        super().__init__()
        self.log_path = log_path
        self.logs = logs
        self.detailed = detailed

    def compose(self) -> ComposeResult:
        # Create the content for the modal (error message and OK button)
        if self.detailed:
            self.log_path += "/detailed_log.txt"
            yield Container(
                Label("Insert the filepath and filename for the export"),
                Input(value=self.log_path, id="path", validate_on=["changed"]),
                Button("Copy to clipboard", variant="primary", id="copy_button"),
                classes="center",
            )
        else:
            yield Container(
                Label("Insert the path for the export folder"),
                Input(value=self.log_path, id="from_time", validate_on=["changed"]),
                Button("Copy to clipboard", variant="primary", id="copy_button"),
                classes="center",
            )
        with Horizontal(classes="center"):
            yield Button.success("Export", id="export")
            yield Button.error("Cancel", id="cancel")

    def on_input_changed(self, event: Input.Changed):
        self.log_path = event.value

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "export":
            if self.detailed:
                log_path = ""
                if "/" in self.log_path:
                    log_path = "/".join(self.log_path.split("/")[:-1])

                if not os.path.exists(log_path):
                    os.makedirs(log_path)
                file = open(self.log_path, "w")
                file.write("UTC Date-Time: " + str(self.logs[0]) + "\n")
                file.write("Local Date-Time: " + str(self.logs[1]) + "\n")
                file.write("Status: " + str(self.logs[2]) + "\n")
                file.write("Log message: " + str(self.logs[3]) + "\n")
                file.close()
            else:
                if not os.path.exists(self.log_path):
                    os.makedirs(self.log_path)
                for nr, log in enumerate(self.logs):
                    file = open(self.log_path + "/log_" + str(nr + 1) + ".txt", "w")
                    file.write("UTC Date-Time: " + str(log[0]) + "\n")
                    file.write("Local Date-Time: " + str(log[1]) + "\n")
                    file.write("Status: " + str(log[2]) + "\n")
                    file.write("Log message: " + str(log[3]) + "\n")
                    file.close()
            self.app.pop_screen()

        if event.button.id == "cancel":
            self.app.pop_screen()
        if event.button.id == "copy_button":
            self.app.copy_to_clipboard(self.log_path)
