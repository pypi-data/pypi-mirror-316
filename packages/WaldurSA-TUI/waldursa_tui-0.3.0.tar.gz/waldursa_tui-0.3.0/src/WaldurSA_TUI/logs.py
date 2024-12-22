from textual.app import ComposeResult
from textual.widgets import (
    ListView,
    ListItem,
    Label,
    Input,
    DataTable,
    Button,
    Rule,
    Select,
)
from textual import on
from textual.containers import Container, Vertical, Horizontal
from textual_datepicker import DateSelect
from textual.worker import Worker, WorkerState
from textual.reactive import reactive
from rich.text import Text
from textual import work
from WaldurSA_TUI import error, detailed_log, log_export_path

import subprocess
import json

from datetime import datetime
import re


class LabelItem(ListItem):
    def __init__(self, content: str) -> None:
        super().__init__()

        self.content = content

    def compose(self) -> ComposeResult:
        yield Label(self.content, id="side_menu_logs_button")

    def get_content(self):
        return self.content


class Logs(Container):
    countdown = reactive(30)

    def __init__(self):
        super().__init__()

        self.list_view_menu = ListView(classes="box", id="side_menu_logs")
        self.search_bar = Input(placeholder="Search...", id="search_bar_logs")
        self.drop_down = Select(
            options=[
                ("info", "info"),
                ("error", "error"),
                ("exception", "exception"),
                ("warning", "warning"),
                ("unknown", "unknown"),
            ],
            prompt="Status",
            id="filter_status",
        )

        self.logs_filtered = []
        self.logs_buffer = []

        self.selectedView = "Processing Orders"  # the default view
        self.dataTable = DataTable(id="logs_table")

        self.batch_size = 300

        self.log_worker = None

        self.refresh_button = Button(
            "Refreshing in " + str(self.countdown) + "s", id="refresh"
        )
        self.newest_oldest_button = Button("Sort by: Oldest", id="newest_oldest")
        self.refresh_status = "stopped"
        self.no_logs_status = True

        self.fromtime = ""
        self.totime = ""
        self.reverse_sort = False
        self.search_bar_value = ""
        self.status_filter = False
        self.status_filter_value = ""
        self.since = ""
        self.until = ""

    def compose(self) -> ComposeResult:
        yield self.list_view_menu
        with Vertical(id="logdates"):
            with Horizontal(classes="height-auto width-full margin-bottom-1"):
                with Horizontal(classes="height-auto left-align"):
                    yield DateSelect(
                        placeholder="From date",
                        format="YYYY-MM-DD",
                        picker_mount="#logdates",
                        classes="column",
                        id="from_date",
                    )
                    yield DateSelect(
                        placeholder="To date",
                        format="YYYY-MM-DD",
                        picker_mount="#logdates",
                        classes="column",
                        id="to_date",
                    )
                with Horizontal(classes="height-auto right-align"):
                    yield Input(
                        placeholder="From: xx:xx",
                        id="from_time",
                        validate_on=["changed"],
                    )
                    yield Input(
                        placeholder="To: xx:xx", id="to_time", validate_on=["changed"]
                    )

            with Horizontal(classes="height-auto width-full"):
                with Horizontal(classes="height-auto left-align leftSearch"):
                    yield self.search_bar
                with Horizontal(classes="height-auto right-align rightSort"):
                    yield self.drop_down
                    yield self.newest_oldest_button
                    yield Button(
                        "Clear filters", id="clear_filter", classes="margin-left-1"
                    )

            with Horizontal(classes="height-auto width-full"):
                with Horizontal(classes="height-auto left-align margin-left-1"):
                    yield Button("Search", id="search", classes="margin-right-1")
                    yield self.refresh_button
                with Horizontal(classes="height-auto right-align"):
                    yield Button(
                        "Export", id="export", classes="margin-left-1"
                    )  # OK button to close the popup

            yield Rule(line_style="heavy")
            yield self.dataTable
            yield Label(
                "Apply filters and press Search to see results", id="logs_no_results"
            )

    async def on_mount(self):
        await self.make_listView_menu(await self.left_menu())
        self.dataTable.cursor_type = "row"
        self.dataTable.add_columns("UTC Date", "Local Date", "Status", "Log")

        self.timer = self.set_interval(1, self.tick)

    def tick(self) -> None:
        if self.refresh_status == "started":
            self.countdown = self.countdown - 1
            self.refresh_button.label = "Refreshing in " + str(self.countdown) + "s"
            if self.countdown == 0:
                self.countdown = 30
                self.dataTable.loading = True

                date_select_from = self.query_one("#from_date")
                date_select_to = self.query_one("#to_date")

                if self.get_dates(date_select_from, date_select_to):
                    self.start_log_worker()

    async def left_menu(
        self,
    ):  # if there are more than these three options, it will be removed/changed
        return [
            "Processing Orders",
            "User Membership Synchronization",
            "Usage Reporting",
        ]

    async def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        if event.state == WorkerState.SUCCESS and event.worker.group == "getLogs":
            self.cancel_log_worker()

    async def append_table(self, new_logs):
        self.dataTable.loading = False
        self.dataTable.add_rows(new_logs)

    @work(exclusive=True, thread=True, group="getLogs")
    async def load_logs(self, side_menu_text):
        self.logs_filtered.clear()
        self.logs_buffer.clear()
        self.dataTable.clear()
        cursor = None
        while True:
            logs, cursor = self.get_logs(side_menu_text, cursor)
            if logs == []:
                break
            self.filter_logs(logs)
            self.app.call_from_thread(self.append_table, self.logs_buffer)
            self.logs_buffer.clear()

    # Filter logs based on search bar and status filter
    def filter_logs(self, logs):
        if self.status_filter:
            temp = [
                log
                for log in logs.copy()
                if self.status_filter_value == "info"
                and str(log[2]).lower() == "info"
                or self.status_filter_value == "error"
                and str(log[2]).lower() == "error"
                or self.status_filter_value == "exception"
                and str(log[2]).lower() == "exception"
                or self.status_filter_value == "warning"
                and str(log[2]).lower() == "warning"
                or self.status_filter_value == "unknown"
                and str(log[2]).lower() == "unknown"
            ]
        else:
            temp = logs.copy()

        for log in temp:
            if self.search_bar_value.lower() in str(log[3]).lower():
                self.logs_filtered.append(log)
                self.logs_buffer.append(log)

    # Get logs from journalctl
    def get_logs(self, side_menu_text, cursor=None):
        filters = " --utc"

        if side_menu_text == "Processing Orders":
            filters += " -u waldur-agent-order-process.service"
        elif side_menu_text == "User Membership Synchronization":
            filters += " -u waldur-agent-membership-sync.service"
        elif side_menu_text == "Usage Reporting":
            filters += " -u waldur-agent-report.service"

        if self.reverse_sort:
            filters += " -r"
            filters += " -n " + str(self.batch_size)
        else:
            filters += " -n +" + str(
                self.batch_size
            )  # plus in front of number is needed!

        if self.since != "":
            filters += self.since
        if self.until != "":
            filters += self.until

        if cursor is not None:
            filters += ' --after-cursor="' + cursor + '"'

        result = subprocess.run(
            "journalctl -o json"
            + filters
            + " --output-fields=__REALTIME_TIMESTAMP,MESSAGE,__CURSOR --no-pager",
            shell=True,
            capture_output=True,
            text=True,
        )

        json_output = f"[{','.join(result.stdout.splitlines())}]"
        logs_json = json.loads(json_output)

        if logs_json == []:
            return ([], "")

        cursor = logs_json[-1]["__CURSOR"]

        def unix_to_time(unix_time):
            return datetime.fromtimestamp(int(unix_time) / 1000000).strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        pattern = re.compile(r"\[(.*)\]\s+\[(.*)\]\s+(.*)")
        logs = []
        for i in range(len(logs_json)):
            matches = re.match(pattern, logs_json[i]["MESSAGE"])
            if matches:
                log_level, timestamp, message = matches.groups()
                if (
                    log_level.lower() == "error"
                    or log_level.lower() == "exception"
                    or "error" in message.lower()
                ):
                    logs.append(
                        (
                            Text(
                                unix_to_time(logs_json[i]["__REALTIME_TIMESTAMP"]),
                                style="red",
                            ),
                            Text(timestamp.split(",")[0], style="red"),
                            Text(log_level, style="red"),
                            Text(message, style="red"),
                        )
                    )
                elif log_level.lower() == "warning" or "warning" in message.lower():
                    logs.append(
                        (
                            Text(
                                unix_to_time(logs_json[i]["__REALTIME_TIMESTAMP"]),
                                style="yellow",
                            ),
                            Text(timestamp.split(",")[0], style="yellow"),
                            Text(log_level, style="yellow"),
                            Text(message, style="yellow"),
                        )
                    )
                else:
                    logs.append(
                        (
                            Text(unix_to_time(logs_json[i]["__REALTIME_TIMESTAMP"])),
                            Text(timestamp.split(",")[0]),
                            Text(log_level),
                            Text(message),
                        )
                    )
            else:
                logs.append(
                    (
                        Text(unix_to_time(logs_json[i]["__REALTIME_TIMESTAMP"])),
                        Text(unix_to_time(logs_json[i]["__REALTIME_TIMESTAMP"])),
                        Text("UNKNOWN"),
                        Text(logs_json[i]["MESSAGE"]),
                    )
                )

        return (logs, cursor)

    def cancel_log_worker(self):
        if self.log_worker is not None:
            self.log_worker.cancel()
        self.log_worker = None

    def start_log_worker(self):
        self.cancel_log_worker()
        self.log_worker = self.load_logs(self.selectedView)

    async def on_list_view_selected(self, event: ListView.Selected):
        if event.list_view.id == "side_menu_logs":
            side_menu_text = event.item.get_content()
            self.selectedView = side_menu_text

            self.cancel_log_worker()

            self.logs_filtered.clear()
            self.dataTable.clear()

            if self.no_logs_status:
                await self.query_one("#logs_no_results").remove()
                self.no_logs_status = False

            no_logs = Label(
                "Apply filters and press Search to see results", id="logs_no_results"
            )
            self.no_logs_status = True
            self.query_one(DataTable).mount(no_logs, after=self.query_one(DataTable))

    async def on_input_changed(self, event: Input.Changed):
        if event.input.id == "search_bar_logs":
            self.search_bar_value = event.value
        if event.input.id == "from_time":
            self.fromtime = event.value
        if event.input.id == "to_time":
            self.totime = event.value

    # Opens new screen with detailed view of one log when clicked on a log in datatabel
    async def on_data_table_row_selected(self, event: DataTable.RowSelected):
        indx = event.row_key
        log_row = DataTable.get_row(self.dataTable, indx)
        utc_date = log_row[0]
        local_date = log_row[1]
        status = log_row[2]
        log_msg = log_row[3]

        self.app.push_screen(
            detailed_log.DetailedLogPopUp(
                utc_date,
                local_date,
                status,
                log_msg,
            )
        )

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "export":
            self.app.push_screen(
                log_export_path.LogExportPath(
                    "src/test_export_logs", self.logs_filtered, False
                )
            )

        if event.button.id == "refresh":
            if self.refresh_status == "started":
                self.refresh_status = "stopped"
            elif self.refresh_status == "stopped":
                self.refresh_status = "started"

        if event.button.id == "search":
            date_select_from = self.query_one("#from_date")
            date_select_to = self.query_one("#to_date")

            if self.get_dates(date_select_from, date_select_to):
                self.refresh_status = "started"
                self.countdown = 30

                self.dataTable.loading = True

                self.start_log_worker()
                self.dataTable.cursor_coordinate = (0, 0)

        if event.button.id == "clear_filter":
            self.query_one("#from_date").date = None
            self.query_one("#to_date").date = None

            self.query_one("#search_bar_logs").value = ""
            self.query_one("#from_time").value = ""
            self.query_one("#to_time").value = ""
            self.search_bar_value = ""
            self.fromtime = ""
            self.totime = ""

            self.newest_oldest_button.label = "Sort by: Oldest"
            self.reverse_sort = False

            self.query_one("#filter_status").value = self.query_one(
                "#filter_status"
            ).BLANK
            self.status_filter = False

        if event.button.id == "newest_oldest":
            if self.reverse_sort:
                self.newest_oldest_button.label = "Sort by: Oldest"
                self.reverse_sort = False
            else:
                self.newest_oldest_button.label = "Sort by: Newest"
                self.reverse_sort = True

            self.countdown = 30
            self.start_log_worker()

    @on(Select.Changed)
    async def on_select_changed(self, event: Select.Changed) -> None:
        if event.select.id == "filter_status":
            if self.drop_down.value != self.drop_down.BLANK:
                self.status_filter = True
                self.status_filter_value = event.value
            else:
                self.status_filter = False

            self.countdown = 30
            self.start_log_worker()

    async def on_key(self, event) -> None:
        if event.key in ("down", "up"):
            if self.dataTable.has_focus:
                if event.key == "down":
                    self.dataTable.scroll_down()
                elif event.key == "up":
                    self.dataTable.scroll_up()

    async def make_listView_menu(self, list_buttons):
        for button in list_buttons:
            labelItem_button = LabelItem(button)
            self.list_view_menu.append(labelItem_button)

    def check_time(self, time):
        if time == "":
            return False

        pattern = r"(\d\d:\d\d)"
        matches = re.match(pattern, time)
        if matches:
            times = time.split(":")
            if int(times[0]) < 0 or int(times[0]) > 23:
                self.app.push_screen(
                    error.ErrorPopup(
                        "Hours must be between 0 and 23",
                        "Time error",
                    )
                )
                return False
            elif int(times[1]) < 0 or int(times[1]) > 59:
                self.app.push_screen(
                    error.ErrorPopup(
                        "Minutes must be between 0 and 59",
                        "Time error",
                    )
                )
                return False

        else:
            self.app.push_screen(
                error.ErrorPopup(
                    "Inputed time is not a correct",
                    "Input error",
                )
            )
            return False
        return True

    def get_dates(self, date_select_from, date_select_to):
        def convert_to_datetime(time):
            return str(time).split(" ")[0]

        if date_select_from.date is not None and date_select_to.date is not None:
            from_date = convert_to_datetime(date_select_from.date)
            to_date = convert_to_datetime(date_select_to.date)

            if from_date > to_date:
                self.app.push_screen(
                    error.ErrorPopup(
                        "From date is bigger than to date",
                        "Time error",
                    )
                )
                return False

        fromtime = self.check_time(self.fromtime)
        totime = self.check_time(self.totime)

        if date_select_from.date is not None:
            from_date = convert_to_datetime(date_select_from.date)
            if fromtime:
                self.since = ' --since "' + from_date + " " + self.fromtime + '" '
            else:
                self.since = " --since " + from_date + " "

        if date_select_to.date is not None:
            to_date = convert_to_datetime(date_select_to.date)
            if totime:
                self.until = ' --until "' + to_date + " " + self.totime + '" '
            else:
                self.until = " --until " + to_date + " "

        if date_select_to.date is None and totime:
            self.since = " --since " + self.totime + " "

        if date_select_from.date is None and fromtime:
            self.until = " --until " + self.fromtime + " "

        if date_select_from.date is None and date_select_to.date is None:
            if self.fromtime != "" and self.totime != "":
                if fromtime and totime:
                    fromtime_check = int("".join(self.fromtime.split(":")))
                    totime_check = int("".join(self.totime.split(":")))

                    if fromtime_check > totime_check:
                        self.app.push_screen(
                            error.ErrorPopup(
                                "From time is bigger than to time",
                                "Time error",
                            )
                        )
                        return False

            if self.fromtime != "":
                if fromtime:
                    self.since = " --since " + self.fromtime + " "
                else:
                    return False

            if self.totime != "":
                if totime:
                    self.until = " --until " + self.totime + " "
                else:
                    return False
        return True
