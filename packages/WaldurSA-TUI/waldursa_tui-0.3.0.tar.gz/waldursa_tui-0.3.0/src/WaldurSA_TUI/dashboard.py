import datetime
from textual.widgets import DataTable
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual_plotext import PlotextPlot
from textual.reactive import reactive
from rich.text import Text
from collections import deque

import subprocess
import re


class Dashboard(Container):
    countdown = reactive(30)

    def __init__(self):
        super().__init__()

        self.table_columns = (
            "Service",
            "Uptime",
            "On boot",
            "Status",
            "Status details",
        )
        self.service_last_seen = {}
        self.services = [
            "waldur-agent-membership-sync",
            "waldur-agent-order-process",
            "waldur-agent-report",
        ]
        self.service_statuses = []
        self.graphs = {
            "waldur-agent-membership-sync-cpu": deque([], maxlen=300),
            "waldur-agent-membership-sync-memory": deque([], maxlen=300),
            "waldur-agent-order-process-cpu": deque([], maxlen=300),
            "waldur-agent-order-process-memory": deque([], maxlen=300),
            "waldur-agent-report-cpu": deque([], maxlen=300),
            "waldur-agent-report-memory": deque([], maxlen=300),
        }
        self.graph_names = {
            "waldur-agent-membership-sync-cpu": "Membership Sync CPU",
            "waldur-agent-membership-sync-memory": "Membership Sync Memory",
            "waldur-agent-order-process-cpu": "Order Process CPU",
            "waldur-agent-order-process-memory": "Order Process Memory",
            "waldur-agent-report-cpu": "Report CPU",
            "waldur-agent-report-memory": "Report Memory",
        }

    def compose(self) -> ComposeResult:
        with Vertical():
            yield DataTable(id="process_table")
            with Container(classes="dash-graphs"):
                for name in self.graph_names:
                    yield PlotextPlot(id="graph" + name)

    def on_mount(self) -> None:
        for service in self.services:
            self.service_last_seen[service] = -1
        table = self.query_one(DataTable)
        table.cursor_type = "none"
        table.add_columns(*self.table_columns)
        self.get_logs()
        self.render_table()

        for key, val in self.graphs.items():
            plt = self.query_one("#graph" + key).plt
            plt.date_form("H:M:S")
            plt.title(self.graph_names[key])
            if "memory" in key:
                plt.ylabel("MB")
            if "cpu" in key:
                plt.ylabel("%")

        self.timer = self.set_interval(1, self.tick)

    def tick(self) -> None:
        self.countdown = self.countdown - 1
        for service in self.service_last_seen:
            if self.service_last_seen[service] != -1:
                self.service_last_seen[service] += 1
        table = self.query_one(DataTable)
        table.clear()
        self.render_table()

        # Graphs
        for service in self.services:
            self.get_service_usage(service)

        for key, val in self.graphs.items():
            plt = self.query_one("#graph" + key).plt

            metric = [x["value"] for x in val if "value" in x]
            time = [x["time"] for x in val if "time" in x]

            plt.clear_data()
            plt.scatter(time, metric)

        self.refresh()

        if self.countdown == 0:
            self.countdown = 30
            self.get_logs()

    def get_logs(self):
        statuses = []
        for service in self.services:
            status = self.get_systemd_process_status(service)
            if status["status"] == "OK":
                self.service_last_seen[status["name"]] = 0
            statuses.append(status)
        self.service_statuses = statuses

    def render_table(self):
        table = self.query_one(DataTable)

        for status in self.service_statuses:
            if status["status"] == "OK":
                table.add_row(
                    status["name"],
                    status["time"],
                    Text(status["on_boot"], style=status["on_boot_style"]),
                    Text(status["status"], style=status["style"]),
                )
            else:
                table.add_row(
                    status["name"],
                    status["time"],
                    Text(status["on_boot"], style=status["on_boot_style"]),
                    Text(status["status"], style=status["style"]),
                    status["reason"],
                )

    def get_systemd_process_status(self, process_name):
        result = subprocess.run(
            f"systemctl status {process_name} | grep -e 'Active:' -e 'Process:' -e 'Loaded:'",
            shell=True,
            capture_output=True,
            text=True,
        )

        is_found = bool(result.stdout)
        is_failed = self.get_if_process_failed(result.stdout)
        is_active = self.get_if_process_active(result.stdout)

        if not is_found:
            status = "NOT FOUND"
        elif is_failed:
            status = "FAILED"
        elif is_active:
            status = "OK"
        elif not is_active:
            status = "INACTIVE"
        else:
            match = re.search(r"Active: (\S+)", result.stdout)
            if match:
                status = match.group(1).upper()
            else:
                status = "UNKNOWN"

        time_match = re.search(r"since (.*?); (.*? ago)", result.stdout)
        time = time_match.group(2) if time_match else "Unknown"
        on_boot = self.get_process_on_boot(result.stdout)

        return {
            "name": process_name,
            "on_boot": on_boot,
            "on_boot_style": self.get_process_on_boot_color(on_boot),
            "status": status,
            "reason": self.get_process_reason(result.stdout),
            "style": "red" if status != "OK" else "green",
            "time": time,
        }

    def get_service_usage(self, service_name):
        result = subprocess.run(
            "systemd-cgtop -r -n 1 | grep " + service_name,
            shell=True,
            capture_output=True,
            text=True,
        )
        current_time = datetime.datetime.now().strftime("%H:%M:%S")

        if result.returncode != 0 or not result.stdout:
            return

        for key, val in self.graphs.items():
            if key.startswith(service_name):
                if key.endswith("cpu"):
                    cpu_use = result.stdout.split()[2]
                    dict = {
                        "time": current_time,
                        "value": 0.0
                        if cpu_use == "-" or (not cpu_use.isdigit())
                        else float(cpu_use),
                    }
                    val.append(dict)
                else:
                    mem_use = result.stdout.split()[3]
                    dict = {
                        "time": current_time,
                        "value": 0 if (not mem_use.isdigit()) else int(mem_use) >> 20,
                    }
                    val.append(dict)

    def get_process_reason(self, output):
        match = re.search(r"Process:.*\((.*)\)", output)
        if match:
            return match.group(1)

        match_PID = re.search(r"Main PID:.*\((.*)\)", output)
        if match_PID:
            return match_PID.group(1)

        return "Unknown"

    def get_process_on_boot(self, output):
        match = re.search(r"Loaded:.*; (.*);", output)
        if match:
            return match.group(1)

        return "unknown"

    def get_process_on_boot_color(self, result):
        if "enabled" in result:
            return "green"
        elif "disabled" in result:
            return "bright_yellow"
        else:
            return "red"

    def get_if_process_active(self, output):
        match = re.search(r"Active: active", output)
        if match:
            return True

        return False

    def get_if_process_failed(self, output):
        match = re.search(r"Active: failed", output)
        if match:
            return True

        return False
