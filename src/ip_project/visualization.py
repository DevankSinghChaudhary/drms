import matplotlib.pyplot as graph
import pandas as pd
import questionary
from rich.console import Console

console = Console()
DISASTER = "./disaster_metadate.csv"
RESOURCE = "./resource.csv"
SEVERITIES = ["Low", "Medium", "High", "Critical"]


class Visual:
    def _read(self, file: str):
        try:
            if file == DISASTER:
                data = pd.read_csv(file, index_col=None)
                return data.to_dict(orient="records")
            else:
                data = pd.read_csv(file, index_col=None)
                return data.to_dict(orient="list")

        except FileNotFoundError:
            return False

    def resource_visuals(self):
        _data = self._read(file=RESOURCE)

        if _data:
            names = _data["name"]
            quants = _data["quantity"]

            graph.bar(names, quants, color="skyblue")
            graph.xlabel("Available Resources")
            graph.ylabel("Quantities of Available Resources")
            graph.title("Resource Visualization")
            graph.show()

    def severity_visuals(self):
        data = self._read(file=DISASTER)

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
