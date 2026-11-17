from datetime import date

import questionary

from ip_project.database import DrmsDatabase
from ip_project.geo_normal import GeoData
from ip_project.header import header


class DisasterManager:
    def __init__(self) -> None:
        self.DrmsDatabase = DrmsDatabase()

    def total_disasters(self) -> int:
        return self.DrmsDatabase.total_disasters()

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

        self.DrmsDatabase.register_disaster(data=data)
        questionary.press_any_key_to_continue().ask()

    def update_disaster(self, updated_data: dict) -> None:
        header(title="Update Disasters", sub_title="DRMS")

        self.DrmsDatabase.update_disaster(data=updated_data)
        questionary.press_any_key_to_continue().ask()

    def show_disasters(self):
        header(title="Disasters", sub_title="DRMS")

        self.DrmsDatabase._show_disaster()
        questionary.press_any_key_to_continue().ask()
