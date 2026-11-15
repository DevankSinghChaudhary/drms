import json
from urllib.parse import urlencode
from urllib.request import urlopen

import questionary

BASE_URL = "https://lgd-json-api.vercel.app"


class GeoData:
    def get_data(self, endpoint: str, params=None):
        URL = f"{BASE_URL}{endpoint}"
        if params:
            URL += f"?{urlencode(params)}"

        RETRY = 5
        while True:
            RETRY -= 1
            try:
                with urlopen(url=URL, timeout=10) as res:
                    return json.loads(res.read().decode("utf-8"))
            except TimeoutError:
                if RETRY > 0:
                    continue
                else:
                    raise TimeoutError(f"Cannot access {BASE_URL}")

    def ask(self, disaster: str) -> dict:
        states = self.get_data(endpoint="/api/states", params={"limit": 100})

        state_names = []
        for state in states["data"]:
            code = state["code"]
            name = state["name"]
            state_names.append(name)

        style = questionary.Style(
            [
                ("completion-menu.completion", "bg:black fg:white"),
                ("completion-menu.completion.current", "bg:cyan fg:black"),
            ]
        )

        selected_state = questionary.autocomplete(
            f"Select state where {disaster} happened:", choices=state_names, style=style
        ).ask()

        for state in states["data"]:
            if selected_state == state["name"]:
                code = state["code"]

        districts = self.get_data(
            endpoint="/api/districts", params={"stateCode": str(code), "limit": 100}
        )

        districts_name = []
        for district in districts["data"]:
            districts_name.append(district["name"])

        selected_district = questionary.autocomplete(
            f"Select city in {selected_state}:", choices=districts_name, style=style
        ).ask()

        return {"state": selected_state, "district": selected_district}
