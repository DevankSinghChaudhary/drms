import pandas as pd
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

DISASTERS = "./disaster_metadate.csv"

console = Console()


class DisasterCsv:
    def _read(self):
        try:
            data = pd.read_csv(DISASTERS, index_col=None)
            return data.to_dict(orient="records")

        except FileNotFoundError:
            return False

    def _check_duplication(self, disaster: dict):
        already_registered = self._read()

        new = []
        if already_registered:
            disaster_copy = disaster.copy()
            del disaster_copy["severity"]
            for ar in already_registered:
                del ar["ID"]
                del ar["severity"]

                new.append(ar)
            if disaster_copy not in new:
                return True
        else:
            return True

    def register_disaster(self, disaster: dict) -> None:
        reg_disaster = self._read()
        duplication = self._check_duplication(disaster=disaster)

        if reg_disaster:
            id = len(reg_disaster) + 1
        else:
            id = 1

        if duplication:
            if isinstance(reg_disaster, list):
                disaster["ID"] = id
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
                disaster["ID"] = id
                disaster_df = pd.DataFrame([disaster])
                disaster_df.to_csv(DISASTERS, index=False)

                console.print(
                    Panel(
                        f"[green]Date Registered: {disaster['date_registered']}\nDisaster: {disaster['disaster_type']}\nLocation: {disaster['location']}\nSeverity: {disaster['severity']}[/green]",
                        title="Disaster Registered",
                        border_style="green",
                    )
                )
        else:
            console.print(
                Panel(
                    f"[white]Date Registered: {disaster['date_registered']}\nDisaster: {disaster['disaster_type']}\nLocation: {disaster['location']}\nSeverity: {disaster['severity']}[/white]",
                    title="Already Registered",
                    border_style="red",
                )
            )

    def show_disaster(self) -> None:
        disasters = self._read()

        table = Table(
            title="Registered Disasters",
            border_style="red",
            caption="You can allocate resources",
        )

        table.add_column("ID")
        table.add_column("Date Registered")
        table.add_column("Disaster")
        table.add_column("Location")
        table.add_column("Severity")

        if disasters:
            for disaster in disasters:
                table.add_row(
                    str(disaster["ID"]),
                    disaster["date_registered"],
                    disaster["disaster_type"],
                    disaster["location"],
                    disaster["severity"],
                )

            console.print(table)
        else:
            console.print("[red]Register disaster to show.[/red]")

    def delete_disaster(self, id: int) -> None:
        register_disaster = self._read()

        new = []
        _id = 1

        if register_disaster:
            for rd in register_disaster:
                if rd["ID"] == int(id):
                    console.print(
                        Panel(
                            f"ID: {rd['ID']}\nDate: {rd['date_registered']}\nDisaster: {rd['disaster_type']}\nLocation: {rd['location']}\nSeverity: {rd['severity']}",
                            title="Disaster Deleted",
                            border_style="yellow",
                        )
                    )
                    del rd
                else:
                    rd["ID"] = _id
                    _id += 1
                    new.append(rd)
            disaster_df = pd.DataFrame(new)
            disaster_df.to_csv(DISASTERS, index=False)

    def total_records(self) -> int | None:
        data = self._read()
        if data:
            return len(data)
        else:
            return None

    def update_disaster(self, id: int, data: dict) -> None:
        register_disasters = self._read()

        if register_disasters:
            for rd in register_disasters:
                if rd.get("ID") == int(id):
                    rd.update(data)
                    break

            disaster_df = pd.DataFrame(register_disasters)
            disaster_df.to_csv(DISASTERS, index=False)

        else:
            console.print("[red]Cannot update non-existing record[/red]")
