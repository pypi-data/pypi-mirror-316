from textual.app import ComposeResult
from textual.widgets import ListView, ListItem, Label, Input, DataTable
from textual.containers import Container, Vertical
from textual.worker import Worker, WorkerState, get_current_worker
from textual import work
import subprocess

import re
import yaml


class LabelItem(ListItem):
    def __init__(self, content: str) -> None:
        super().__init__()

        self.content = content

    def compose(self) -> ComposeResult:
        yield Label(self.content, id="side_menu_offerings_button")

    def get_content(self):
        return self.content


class Configured_offerings(Container):
    def __init__(self):
        super().__init__()

        self.side_menu = ListView(classes="box", id="side_menu_offerings_listview")
        self.search_bar = Input(placeholder="Search...", id="search_bar_offerings")
        self.dataTable = DataTable(id="data_table_offerings")
        self.offering_buttons = []
        self.offerings = set()
        self.display_worker = None
        self.services = [
            "waldur-agent-membership-sync",
            "waldur-agent-order-process",
            "waldur-agent-report",
        ]
        self.token = "Test"
        self.selected_offering = None

    def compose(self) -> ComposeResult:
        with Vertical(id="side_menu_offerings"):
            yield self.search_bar
            yield self.side_menu
        yield self.dataTable

    async def initialize_table(self, offering_name):
        offering = self.get_offering_by_name(offering_name, self.offerings)
        if offering is None:
            return

        self.dataTable.add_row("waldur_api_url", offering["waldur_api_url"])
        self.dataTable.add_row("waldur_api_token", "******************************")
        self.token = offering["waldur_api_token"]
        self.dataTable.add_row("waldur_offering_uuid", offering["waldur_offering_uuid"])

        self.dataTable.add_row("backend_type", offering["backend_type"])
        for key in offering["backend_settings"]:
            self.dataTable.add_row(key, offering["backend_settings"][key])
        for key in offering["backend_components"]:
            self.dataTable.add_row(key, offering["backend_components"][key])

    async def read_offerings(self, path):
        with open(path, "r") as file:
            yaml_loaded = yaml.safe_load(file)
            return yaml_loaded["offerings"]

    def get_offering_by_name(self, name, offerings):
        for offering in offerings:
            if offering["name"] == name:
                return offering
        return None

    @work(exclusive=True, thread=True, group="getOfferings")
    async def find_and_get_offerings(self):
        is_file_found = False
        for service in self.services:  # for each service
            # find commang used to start the service
            result = subprocess.run(
                f"systemctl status {service} | grep 'CGroup:' -A 2",
                shell=True,
                capture_output=True,
                text=True,
            )

            # extract file path from the result
            match = re.search(r"-c (\S+)", result.stdout)
            if match:
                file = match.group(1)
                is_file_found = True
                break

        # if file is found, read the offerings from the file
        if not get_current_worker().is_cancelled and is_file_found:
            self.offerings = await self.read_offerings(file)

    async def on_list_view_selected(self, event: ListView.Selected):
        if event.list_view.id == "side_menu_offerings_listview":
            self.selected_offering = event.item

            side_menu_text = event.item.get_content()
            self.dataTable.clear()
            await self.initialize_table(side_menu_text)

    async def on_data_table_cell_selected(self, event: DataTable.CellSelected):
        row = event.cell_key[0]
        column = event.cell_key[1]
        selected_cell = DataTable.get_cell(self.dataTable, row, column)
        if selected_cell == "******************************":
            DataTable.update_cell(self.dataTable, row, column, self.token)
        elif selected_cell == self.token:
            DataTable.update_cell(
                self.dataTable, row, column, "******************************"
            )

    async def on_input_submitted(self, event: Input.Submitted):
        input_text = event.value.lower()
        side_menu = self.query_one("#side_menu_offerings_listview", ListView)

        if input_text == "":
            for i in range(len(self.offering_buttons)):
                if self.offering_buttons[i] not in side_menu.children:
                    self.side_menu.append(self.offering_buttons[i])

                    if self.selected_offering is self.offering_buttons[i]:
                        for j in range(len(side_menu.children)):
                            if self.offering_buttons[i] == side_menu.children[j]:
                                side_menu.index = j
                    else:
                        self.offering_buttons[i].highlighted = False
        else:
            for i in range(len(self.offering_buttons)):
                if input_text in self.offering_buttons[i].get_content().lower():
                    if self.offering_buttons[i] not in side_menu.children:
                        side_menu.append(self.offering_buttons[i])

                        if self.selected_offering is self.offering_buttons[i]:
                            for j in range(len(side_menu.children)):
                                if self.offering_buttons[i] == side_menu.children[j]:
                                    side_menu.index = j
                        else:
                            self.offering_buttons[i].highlighted = False
                else:
                    for j in range(len(side_menu.children)):
                        if self.offering_buttons[i] == side_menu.children[j]:
                            if self.selected_offering is not self.offering_buttons[i]:
                                side_menu.children[j].highlighted = False

                            side_menu.remove_items(iter([j]))
                            break

    async def on_mount(self):
        self.side_menu.loading = True
        self.find_and_get_offerings()
        self.dataTable.add_columns("Item", "Value")

    async def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        if event.state == WorkerState.SUCCESS and event.worker.group == "getOfferings":
            if self.display_worker is not None:
                if self.display_worker.is_running:
                    self.display_worker.cancel()
                self.display_worker = None

            self.display_worker = self.run_worker(
                self.display_offerings(), exclusive=True
            )

    async def display_offerings(self):
        list = self.side_menu
        list.clear()
        await self.make_listView_menu(self.offerings)
        if len(list.children) > 0:
            await self.initialize_table(list.children[0].get_content())
        list.loading = False

    async def make_listView_menu(self, offerings):
        i = 0
        for offering in offerings:
            labelItem_button = LabelItem(offering["name"])

            self.side_menu.append(labelItem_button)
            self.offering_buttons.append(labelItem_button)

            if self.selected_offering is None:
                self.selected_offering = labelItem_button
                self.side_menu.index = i

            i += 1
