import json
from datetime import date
from json.decoder import JSONDecodeError

import questionary
from rich.console import Console
from rich.panel import Panel

from ip_project.geo_normal import GeoData
from ip_project.header import header

DATA = "./data"


console = Console()


class Disaster:
    def _load(self):
        try:
            with open(f"{DATA}/disaster_metadata.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError, JSONDecodeError:
            return False

    def _check_duplication(self, date: str, location: dict, d_type: str):
        disasters = self._load()
        comp2 = {
            "disaster_type": d_type.lower(),
            "state": location["state"],
            "district": location["district"],
            "date": date,
        }
        if disasters:
            for disaster in disasters:
                comp = {}
                comp["disaster_type"] = disaster["disaster_type"]
                comp["state"] = disaster["location"]["state"]
                comp["district"] = disaster["location"]["district"]
                comp["date"] = disaster["date_registered"]

                if comp == comp2:
                    return False
                else:
                    return True
        else:
            return True

    def register(self):
        header(title="Register Disaster", sub_title="DRMS")

        try:
            with open(f"{DATA}/disaster_metadata.json", "r", encoding="utf-8") as f:
                td = json.load(f)
            if isinstance(td, dict):
                td = [td]
        except FileNotFoundError, JSONDecodeError:
            td = []

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

        confirmation = self._check_duplication(
            date=str(date.today()), location=location, d_type=disaster_type
        )
        if confirmation:
            disaster = {
                "date_registered": str(date.today()),
                "disaster_type": disaster_type.lower(),
                "location": location,
                "severity": severity.lower(),
            }

            td.append(disaster)
            console.print(
                Panel(
                    f"Type: {disaster_type}\nState: {location['state']}\nDistrict: {location['district']}\nSeverity: {severity}",
                    title="Disaster Registered",
                    border_style="green",
                )
            )
            with open(f"{DATA}/disaster_metadata.json", "w", encoding="utf-8") as f:
                json.dump(td, f)

        else:
            console.print(
                Panel(
                    f"[yellow]Already Registered this Disaster: {disaster_type} in {location['district']}, {location['state']} at {date.today()}[/yellow]"
                )
            )
        questionary.press_any_key_to_continue().ask()
