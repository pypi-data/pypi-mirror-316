from textual.app import App, ComposeResult
from textual.widgets import TabbedContent, TabPane, Footer

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from WaldurSA_TUI import (
    configured_offerings,
    dashboard,
    logs,
    quit,
)

"""import configured_offerings
import dashboard
import logs

import quit
import error"""


class WaldurSATUIApp(App):
    CSS_PATH = "main.tcss"
    BINDINGS = [
        ("escape", "request_quit", "Quit"),
        ("q", "request_quit", "Quit"),
    ]

    def __init__(self):
        super().__init__()

        self.last_tab = "--content-tab-dashboard"

    def compose(self) -> ComposeResult:
        with TabbedContent(initial="dashboard"):
            with TabPane("Dashboard", id="dashboard"):
                yield dashboard.Dashboard()
            with TabPane("Logs", id="logs"):
                yield logs.Logs()
            with TabPane("Configured offerings", id="configured_offerings"):
                yield configured_offerings.Configured_offerings()
            yield TabPane("Exit", id="exit")
        yield Footer()

    def on_tabbed_content_tab_activated(self, event: TabbedContent.TabActivated):
        if event.tab.id == "--content-tab-exit":
            self.action_request_quit()
        else:
            self.last_tab = event.tab.id.split("-")[-1]

    def action_request_quit(self) -> None:
        """Action to display the quit dialog."""

        def check_quit(quit: bool) -> None:
            """Called when QuitScreen is dismissed."""
            if quit:
                self.exit()
            else:
                self.query_one(TabbedContent).active = self.last_tab

        self.push_screen(quit.QuitScreen(), check_quit)


def main():
    app = WaldurSATUIApp()
    app.run()


if __name__ == "__main__":
    main()
