import pandas as pd
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

RESOURCES = "./resources.csv"

console = Console()


class ResourceCsv:
    def _read(self) -> dict | None:
        try:
            data = pd.read_csv(RESOURCES, index_col=None)
            return data.to_dict(orient="list")

        except FileNotFoundError:
            return None

    def _check_duplication(self, resource: dict):
        already_registered = self._read()

        if already_registered:
            for names in already_registered["names"]:
                if names not in resource["names"]:
                    return True
        else:
            return True

    def register_disaster(self, resource: dict) -> None:
        reg_resource = self._read()
        duplication = self._check_duplication(resource=resource)

        if duplication:
            if isinstance(reg_resource, dict):
                resource_df = pd.DataFrame(resource)
                resource_df.to_csv(RESOURCES)
                console.print(
                    Panel(
                        f"[green]Resources: {resource['names']}\nQuantity: {resource['quants']}[/green]",
                        title="Resources Successfully Registered",
                        border_style="green",
                    )
                )
        else:
            console.print("[yellow]Already Registered[/yellow]")

    def show_resource(self) -> None:
        resource = self._read()

        table = Table(
            title="Registered Resources",
            border_style="yellow",
        )

        table.add_column("ID")
        table.add_column("Resource Name")
        table.add_column("Quantity")

        if resource:
            id = resource["ID"]
            names = resource["names"]
            quants = resource["quants"]

            values = list(zip(id, names, quants))

            for value in values:
                table.add_row(value)

            console.print(table)
        else:
            console.print("[red]Register Resource First to Show[/red]")

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
