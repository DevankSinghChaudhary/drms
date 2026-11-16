from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ip_project.header import header
from ip_project.resource import Resource

console = Console()
table = Table()


class RA:
    def resource_allocation(self):
        header(title="Resource Allocation", sub_title="To Disaster Location")

        resource = Resource()

        resources = resource._load_resource(file="resources")
        disaster_meta = resource._load_resource(file="disaster_metadata")

        if disaster_meta and resources:
            total_d = len(disaster_meta)
            console.print(
                Panel(f"[red]Total Disasters: {total_d}[/red]", border_style="red")
            )

            table.add_column("Date Registered", justify="right", style="cyan")
            table.add_column("Disaster", justify="center")
            table.add_column("State", justify="right")
            table.add_column("District", justify="right")
            table.add_column("Severity", justify="right", style="yellow")

            for disaster in disaster_meta:
                d_type = disaster["disaster_type"]
                date = disaster["date_registered"]
                state = disaster["location"]["state"]
                district = disaster["location"]["district"]
                severity = disaster["severity"]

                table.add_row(date, d_type, state, district, severity)
            console.print(table)

        else:
            console.print(
                Panel(
                    "[green]No Disasters Registered\nRegister to Allocate Resources[/green]",
                    border_style="green",
                )
            )


d = RA()
d.resource_allocation()
