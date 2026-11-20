from datetime import date

import questionary
from rich.console import Console

from ip_project.database import DisasterCsv
from ip_project.geo import GeoData
from ip_project.header import header

console = Console()


class DisasterManager:
    def __init__(self) -> None:
        self.DisasterCsv = DisasterCsv()

    def total_disasters(self) -> int | None:
        return self.DisasterCsv.total_records()

    def register(self) -> None:
        header(title="Register Disaster", sub_title="DRMS")

        RD_CHOICES = [
            "Earthquake",
            "Flood",
            "WildFire",
            "Tsunami",
            "Drought",
            "Landslide",
        ]
        disaster_type = questionary.select(
            "Register Disaster:", choices=RD_CHOICES
        ).ask()

        if disaster_type is None:
            return

        geo = GeoData()
        location = geo.ask(disaster=disaster_type)

        if location is None:
            return

        severity = questionary.select(
            "Select severity:", choices=["Low", "Medium", "High", "Critical"]
        ).ask()

        if severity is None:
            return

        data = {
            "date_registered": str(date.today()),
            "disaster_type": disaster_type,
            "location": location["location"],
            "severity": severity,
        }

        self.DisasterCsv.register_disaster(disaster=data)
        questionary.press_any_key_to_continue().ask()

    def update_disaster(self) -> None:
        header(title="Update Disasters", sub_title="DRMS")
        total_records = self.DisasterCsv.total_records()
        if total_records:
            ID = []
            for i in range(total_records + 1):
                if i == 0:
                    pass
                else:
                    ID.append(str(i))
            print()
            self.show_disasters()
            selected_id = questionary.select("Select ID to Update:", choices=ID).ask()
            fields = questionary.checkbox(
                f"Select What to update in {selected_id} (Date Registered will be auto-updated):",
                choices=["Disaster Type", "Location", "Severity"],
            ).ask()

            data = {}
            if "Disaster Type" in fields:
                RD_CHOICES = [
                    "Earthquake",
                    "Flood",
                    "WildFire",
                    "Tsunami",
                    "Drought",
                    "Landslide",
                ]
                disaster_type = questionary.select(
                    "Register Disaster:", choices=RD_CHOICES
                ).ask()

                if disaster_type is None:
                    return
                data["disaster_type"] = disaster_type

            if "Location" in fields:
                geo = GeoData()
                location = geo.ask()

                if location is None:
                    return
                data["location"] = location["location"]

            if "Severity" in fields:
                severity = questionary.select(
                    "Select severity:", choices=["Low", "Medium", "High", "Critical"]
                ).ask()

                if severity is None:
                    return
                data["severity"] = severity

            data["date_registered"] = str(date.today())

            self.DisasterCsv.update_disaster(id=selected_id, data=data)
        else:
            console.print("[red]No disaster to update[/red]")
        questionary.press_any_key_to_continue().ask()

    def show_disasters(self):
        header(title="Disasters", sub_title="DRMS")

        self.DisasterCsv.show_disaster()

    def delete_disaster(self):
        total_records = self.total_disasters()
        if total_records:
            ID = []
            for i in range(total_records + 1):
                if i == 0:
                    pass
                else:
                    ID.append(str(i))
            print()
            self.show_disasters()
            _id = questionary.select(
                "Which disaster record to delete:", choices=ID
            ).ask()

            self.DisasterCsv.delete_disaster(id=_id)
        else:
            console.print("[red]Register to delete[/red]")


def disaster():
    disaster = DisasterManager()

    CHOICES = ["Register Disaster", "Update Disaster", "Delete Disaster"]

    disaster.show_disasters()
    print()
    console.print("[cyan]Showing so you can take better decision.[/cyan]")

    choice = questionary.select(
        "Operations you can do in Disaster:",
        choices=CHOICES,
    ).ask()

    if choice == CHOICES[0]:
        disaster.register()

    elif choice == CHOICES[1]:
        disaster.update_disaster()

    elif choice == CHOICES[2]:
        disaster.delete_disaster()
