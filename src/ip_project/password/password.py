import time

import questionary
from rich.console import Console
from yaspin import yaspin

from ip_project.header import header

console = Console()
PASSWORD = "FISH"


class Password:
    def __init__(self):
        self.TOTAL_TRIES = 5
        self.spinner = yaspin(text="Checking DRMS daemons...", color="yellow")

    def header(self):
        header(
            title="Disaster Resource Management System",
            sub_title="Enter Password to Enter",
        )

    def input(self):
        return questionary.password("Enter password to enter DRMS:").ask()

    def check(self):
        while True:
            self.head = self.header()
            console.print(f"[green]Total Tries: {self.TOTAL_TRIES}[/green]")

            while True:
                self.password = self.input()
                if self.password == "":
                    console.print("[red]Password cannot be empty![/red]")
                    continue
                else:
                    break

            if self.password == PASSWORD:
                self.spinner.start()
                time.sleep(1)
                self.spinner.ok("✔ ")
                console.print("[green]Welcome to DRMS[/green]")
                time.sleep(1)
                self.spinner.stop()
                return True
            else:
                self.TOTAL_TRIES = self.TOTAL_TRIES - 1
                if self.TOTAL_TRIES == 0:
                    spinner = yaspin(text="Exiting DRMS", color="red")
                    console.print("[red]YOU ARE NOT AUTHORIZED PERSON.[/red]")
                    spinner.start()
                    time.sleep(1)
                    spinner.stop()
                    break

                else:
                    console.print("[red]Wrong Password. Try Again.[/red]")
                    time.sleep(0.5)
                    continue
