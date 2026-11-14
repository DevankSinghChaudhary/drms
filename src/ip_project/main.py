import json
import time
from datetime import date
from json.decoder import JSONDecodeError
from pathlib import Path

import questionary
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from yaspin import yaspin

from ip_project.password import Password
from ip_project.visualization import data_visualization

spinner = yaspin(color="green")

console = Console()

DATA = "./data"


def header(title: str | int, sub_title: str | int):
    console.clear()
    console.print(
        Panel(
            f"[bold orange1]{title}[/bold orange1]\n[white]{sub_title}[/white]",
            border_style="orange1",
        )
    )


def register_disaster():
    header(title="Register Disaster", sub_title="DRMS")

    try:
        with open(f"{DATA}/disaster_metadata.json", "r", encoding="utf-8") as f:
            td = json.load(f)
        if isinstance(td, dict):
            td = [td]
    except JSONDecodeError:
        td = []

    RD_CHOICES = ["Earthquake", "Flood", "WildFire", "Tsunami", "Drought", "Landslide"]
    disaster_type = questionary.select("Register Disaster:", choices=RD_CHOICES).ask()

    if disaster_type is None:
        return

    location = questionary.text(
        "Enter affected location:", instruction="(e.g., Jaipur, Rajasthan)"
    ).ask()

    if location is None:
        return

    severity = questionary.select(
        "Select severity:", choices=["Low", "Medium", "High", "Critical"]
    ).ask()

    if severity is None:
        return

    console.print(
        Panel(
            f"Type: {disaster_type}\nLocation: {location}\nSeverity: {severity}",
            title="Disaster Registered",
            border_style="green",
        )
    )

    disaster = {
        "date_registered": str(date.today()),
        "disaster_type": disaster_type.lower(),
        "location": location.lower(),
        "severity": severity.lower(),
    }

    td.append(disaster)

    with open(f"{DATA}/disaster_metadata.json", "w", encoding="utf-8") as f:
        json.dump(td, f)

    questionary.press_any_key_to_continue().ask()


def resource_ask():
    return questionary.confirm(
        "You want to add resource:", auto_enter=False, default=False
    ).ask()


class Resource:
    def add_resource(self):
        resources = {}
        r_name = []
        r_quant = []
        number_resources = int(input("Enter number of resources you want to add: "))

        for i in range(number_resources):
            res_name = input(f"Enter Resource name numbered {i + 1}: ")
            res_quant = int(input(f"Enter quantity of {res_name}: "))

            r_name.append(res_name)
            r_quant.append(res_quant)

        resources["name"] = r_name
        resources["quantity"] = r_quant

        with open(f"{DATA}/resources.json", "w", encoding="utf-8") as f:
            json.dump(resources, f)

    def check_resource(self):
        if Path(f"{DATA}/resources.json").exists():
            try:
                with open(f"{DATA}/resources.json", "r", encoding="utf-8") as f:
                    self.resources = json.load(f)

            except JSONDecodeError:
                self.resources = []

            if not isinstance(self.resources, dict) or self.resources is None:
                self.resources = self.add_resource()

        else:
            self.resources = self.add_resource()

    def show_resource(self):

        with open(f"{DATA}/resources.json", "r", encoding="utf-8") as f:
            resources = json.load(f)

        table = Table(title="Available Resources")

        table.add_column("Resource Name", justify="left", style="cyan")
        table.add_column("Resource Quantity", justify="right", style="green")

        name_row = resources["name"]
        quant_row = resources["quantity"]

        total_n = len(name_row)
        total_q = len(quant_row)

        if total_n == total_q:
            for i in range(total_n):
                name = name_row[i - 1]
                quant = quant_row[i - 1]
                table.add_row(name, str(quant))

        console.print(table)


def resource_management():
    header(
        title="Resource Management", sub_title="See all resources available or add any"
    )

    choice = resource_ask()

    resources = Resource()
    if choice:
        resources.check_resource()

    elif choice is False:
        resources.show_resource()
    questionary.press_any_key_to_continue().ask()


def DRMS() -> None:
    _password = Password()
    _password.header()
    if _password.check():
        while True:
            header(
                title="Disaster Resource Management System",
                sub_title="DRMS",
            )
            try:
                with open(f"{DATA}/disaster_metadata.json", "r", encoding="utf-8") as f:
                    total_disasters = json.load(f)

            except FileNotFoundError, JSONDecodeError:
                total_disasters = []

            console.print(
                Panel(
                    f"Toal Disasters Recorded: {len(total_disasters)}",
                    border_style="red",
                )
            )

            CHOICES = [
                "Disaster Registration",
                "Resource Management",
                "Data Visualization",
                "EXIT",
            ]

            choice = questionary.select(
                "What you would like to do?", choices=CHOICES
            ).ask()

            if choice.lower() == "disaster registration":
                register_disaster()

            elif choice.lower() == "resource management":
                resource_management()

            elif choice.lower() == "data visualization":
                data_visualization()

            elif choice.lower() == "exit":
                spinner = yaspin(text="Exiting DRMS", color="red")
                spinner.start()
                time.sleep(1.5)
                spinner.stop()
                break


if __name__ == "__main__":
    DRMS()
