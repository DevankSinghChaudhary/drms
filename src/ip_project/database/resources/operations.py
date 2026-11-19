import pandas as pd
import questionary
from rich.console import Console
from rich.table import Table

from ip_project.header import header

RESOURCE = "./resource.csv"

console = Console()


class ResourceCsv:
    def _load_resource(self, file: str):
        try:
            data = pd.read_csv(file, index_col=None)
            return data.to_dict(orient="list")

        except FileNotFoundError:
            return None

    def ask(self):
        return questionary.confirm(
            "You want to add resource:", auto_enter=False, default=False
        ).ask()

    def add_resource(self):
        resources = self._load_resource(file=RESOURCE)

        if isinstance(resources, dict):
            res_name = resources["name"]
            res_quant = resources["quantity"]

            total_data = len(res_name)
            number_resources = int(
                input("Enter number of resource you want to append: ")
            )

            for i in range(number_resources):
                i = i + 1
                name = input(f"Enter Resource name numbered {total_data + i}: ")
                quant = int(input(f"Enter quantity of {name}: "))

                res_name.append(name)
                res_quant.append(quant)

                resources["name"] = res_name
                resources["quantity"] = res_quant

        elif not resources:
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

        resource_df = pd.DataFrame(resources)
        resource_df.to_csv(RESOURCE, index=False)

    def show_resource(self):
        resources = self._load_resource(file=RESOURCE)

        if resources:
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

        else:
            console.print("[red]No Resource file found[/red]")


def resource_management():
    header(
        title="Resource Management", sub_title="See all resources available or add any"
    )

    resources = ResourceCsv()
    resources.show_resource()
    choice = resources.ask()

    if choice:
        resources.add_resource()
