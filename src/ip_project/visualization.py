import json

import matplotlib.pyplot as graph
import questionary
from rich.console import Console

console = Console()
DATA = "./data"
SEVERITIES = ["Low", "Medium", "High", "Critical"]

errors = (FileNotFoundError, json.JSONDecodeError)


class Visual:
    def load_disasters(self, file: str):
        try:
            with open(f"{DATA}/{file}.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except errors:
            if errors == FileNotFoundError:
                console.print(
                    f"[red]Cannot Visualize {file} as there is no /data/{file}.json[/red]"
                )
            else:
                console.print(
                    f"[red]Cannot Visualize {file} as there is formatting issue in /data/{file}.json[/red]"
                )

    def resource_visuals(self):
        data = self.load_disasters(file="resources")

        if data:
            names = data["name"]
            quants = data["quantity"]

            graph.bar(names, quants, color="skyblue")
            graph.xlabel("Available Resources")
            graph.ylabel("Quantities of Available Resources")
            graph.title("Resource Visualization")
            graph.show()

    def severity_visuals(self):
        data = self.load_disasters(file="disaster_metadata")

        low = []
        med = []
        hig = []
        cri = []

        if data:
            for disaster in data:
                d_type = disaster["disaster_type"]
                location = disaster["location"]
                severity = disaster["severity"].lower()
                if severity == SEVERITIES[0].lower():
                    dis = {"type": d_type, "location": location}
                    low.append(dis)
                elif severity == SEVERITIES[1].lower():
                    dis = {"type": d_type, "location": location}
                    med.append(dis)
                elif severity == SEVERITIES[2].lower():
                    dis = {"type": d_type, "location": location}
                    hig.append(dis)
                elif severity == SEVERITIES[3].lower():
                    dis = {"type": d_type, "location": location}
                    cri.append(dis)

        total_number = [len(low), len(med), len(hig), len(cri)]

        graph.bar(SEVERITIES, total_number)
        graph.grid(True, axis="y")

        graph.xlabel("Severity")
        graph.ylabel("Total Number of Disaster Based on Severity")

        graph.title("Disaster Visualization Based on Severity")
        graph.show()


def data_visualization():
    visual = Visual()
    CHOICES = [
        "Disasters on Severity",
        "Available Resources",
    ]

    rod = questionary.select("What you want to see:", choices=CHOICES).ask()

    if rod == CHOICES[0]:
        visual.severity_visuals()

    elif rod == CHOICES[1]:
        visual.resource_visuals()
