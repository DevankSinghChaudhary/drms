import sqlite3
import time

import questionary
from rich.console import Console
from rich.panel import Panel
from yaspin import yaspin

from ip_project.disaster import DisasterManager
from ip_project.password import Password
from ip_project.resource import resource_management
from ip_project.visualization import data_visualization

spinner = yaspin(color="green")

connection = sqlite3.connect("drms.db")
cursor = connection.cursor()

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


def DRMS() -> None:

    disaster = DisasterManager()

    _password = Password()
    _password.header()
    if _password.check():
        while True:
            header(
                title="Disaster Resource Management System",
                sub_title="DRMS",
            )

            console.print(
                Panel(
                    f"Toal Disasters Recorded: {disaster.total_disasters()}",
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
                disaster.register()

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
