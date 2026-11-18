from datetime import date

import pandas as pd
from rich.console import Console
from rich.panel import Panel

DISASTERS = "./disaster_metadate.csv"


console = Console()


class Csv:
    def _read(self):
        try:
            data = pd.read_csv(DISASTERS, index_col=None)
            return data.to_dict(orient="records")
        except FileNotFoundError:
            return False

    def _check_duplication(self, disaster: dict):
        already_registered = self._read()

        if already_registered:
            if disaster not in already_registered:
                return True
        else:
            return True

    def register_disaster(self, disaster: dict):
        reg_disaster = self._read()
        duplication = self._check_duplication(disaster=disaster)

        if duplication:
            if isinstance(reg_disaster, list):
                reg_disaster.append(disaster)
                disasters = pd.DataFrame(reg_disaster)
                disasters.to_csv(DISASTERS, index=False)

                console.print(
                    Panel(
                        f"[green]Date Registered: {disaster['date_registered']}\nDisaster: {disaster['disaster_type']}\nLocation: {disaster['location']}\nSeverity: {disaster['severity']}[/green]",
                        title="Disaster Registered",
                        border_style="green",
                    )
                )

            else:
                disaster["date_registered"] = [disaster["date_registered"]]
                disaster["disaster_type"] = [disaster["disaster_type"]]
                disaster["location"] = [disaster["location"]]
                disaster["severity"] = [disaster["severity"]]

                disaster_df = pd.DataFrame(disaster)
                disaster_df.to_csv(DISASTERS, index=False)

                console.print(
                    Panel(
                        f"[green]Date Registered: {disaster['date_registered'][0]}\nDisaster: {disaster['disaster_type'][0]}\nLocation: {disaster['location'][0]}\nSeverity: {disaster['severity'][0]}[/green]",
                        title="Disaster Registered",
                        border_style="green",
                    )
                )
        elif duplication is None or False:
            console.print(
                Panel(
                    f"[white]Date Registered: {disaster['date_registered']}\nDisaster: {disaster['disaster_type']}\nLocation: {disaster['location']}\nSeverity: {disaster['severity']}[/white]",
                    title="Already Registered",
                    border_style="red",
                )
            )


csv = Csv()
csv.register_disaster(
    disaster={
        "date_registered": str(date.today()),
        "disaster_type": "cyclone",
        "location": "jaipur,rajasthan",
        "severity": "low",
    }
)
