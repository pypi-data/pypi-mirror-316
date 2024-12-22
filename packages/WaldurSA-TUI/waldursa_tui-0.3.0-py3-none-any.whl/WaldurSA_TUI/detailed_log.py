from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Label
from textual.screen import ModalScreen
from WaldurSA_TUI import log_export_path


class DetailedLogPopUp(ModalScreen):
    "Detailed view of a log."

    def __init__(
        self, utc_date: str, local_date: str, status: str, log_msg: str
    ) -> None:
        super().__init__()
        self.utc_date = utc_date
        self.local_date = local_date
        self.status = status
        self.log_msg = log_msg

    def compose(self) -> ComposeResult:
        # Create the content for the modal (log details and OK button)
        with Horizontal():
            with Vertical():
                yield Container(
                    Label("UTC Date       Time", id="date_label_utc"),
                    Label(self.utc_date, id="date_utc"),
                    Label("Local Date       Time", id="date_label_local"),
                    Label(self.local_date, id="date_local"),
                )
            with Vertical():
                yield Container(
                    Label("Status", id="status_label"),
                    Label(self.status, id="status"),
                )

        yield Container(
            Label("Log message", id="log_message"),
            Label(self.log_msg, id="log"),  # Display the log message
        )
        with Horizontal(classes="center"):
            yield Button.success(
                "OK", id="close_button"
            )  # OK button to close the popup
            yield Button("Export", variant="primary", id="export_button")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        # Export the log
        if event.button.id == "export_button":
            self.app.push_screen(
                log_export_path.LogExportPath(
                    "src/test_export_logs",
                    [self.utc_date, self.local_date, self.status, self.log_msg],
                    True,
                )
            )

        # Close the popup when OK button is pressed
        if event.button.id == "close_button":
            self.app.pop_screen()
