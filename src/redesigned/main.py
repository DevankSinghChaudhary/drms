import time
from datetime import date
from typing import Literal

import matplotlib.pyplot as graph
import pandas as pd

DISASTER = "./disasters_metadata.csv"
RESOURCE = "./resources.csv"
PASSWORD = "ADK"


def header(title: str, sub_title: str) -> None:
    title_width = 50 - len(title) - 5
    stitle_width = 50 - len(sub_title) - 5

    print("=" * 50)
    print("|", title, " " * title_width, "|")
    print("|", sub_title, " " * stitle_width, "|")
    print("=" * 50)
    print()
    print()


def ask_loop(prompt: str, func=str):
    while True:
        try:
            print("-" * 40)
            answer = func(input(prompt))
            if answer == "":
                print("Input cannot be empty!")
                tclean()
                continue
            else:
                return answer
                break
        except ValueError:
            print("\nCannot Enter String in Number Place.\nEnter Integer not String.\n")
            continue


def tclean():
    print("\033[2J\033[H", end="")


class Password:
    def __init__(self):
        self.TOTAL_TRIES = 5

    def pass_loop(self):
        while True:
            tclean()
            header(title="Enter Password", sub_title="DRMS")
            print(f"Total Tries: {self.TOTAL_TRIES}")
            while True:
                print("-" * 40)
                answer = input("Enter Password: ")
                if answer == "":
                    print("Input cannot be empty!")
                    time.sleep(0.5)
                    tclean()
                    header(title="Enter Password", sub_title="DRMS")
                    print(f"Total Tries: {self.TOTAL_TRIES}")
                    continue
                else:
                    break
            if answer == PASSWORD:
                time.sleep(0.5)
                print("Welcome to DRMS")
                return True
            else:
                self.TOTAL_TRIES = self.TOTAL_TRIES - 1
                if self.TOTAL_TRIES == 0:
                    print("YOU ARE NOT AUTHORIZED PERSON.")
                    break
                print("Wrong Password. Try Again.")
                time.sleep(0.5)
                continue


class Disaster:
    def _show(self):
        try:
            print(
                pd.read_csv(DISASTER).to_string(
                    index=False, max_colwidth=20, justify="left"
                )
            )
        except FileNotFoundError, pd.pandas.errors.EmptyDataError:
            print("Cannot access Disaster CSV")

    def _read(self) -> list | None:
        try:
            data = pd.read_csv(DISASTER, index_col=False)
            return data.to_dict(orient="records")
        except FileNotFoundError, pd.pandas.errors.EmptyDataError:
            return None

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

    def _ask(self) -> dict:
        print(
            "Disaster Types: [Flood, Tusnami, Drought, Earthquake, Cyclone, Wildfire]"
        )
        print()
        d_type = ask_loop("Enter disaster type (copy from above): ")
        location = ask_loop(f"Enter location of {d_type}: ")
        print()
        print("Severity: [Low, Medium, High, Critical]")
        severity = ask_loop(f"Enter severity of {d_type} (choose from above): ")

        data = {
            "date_registered": str(date.today()),
            "disaster_type": d_type.lower(),
            "location": location.lower(),
            "severity": severity.lower(),
        }
        return data

    def register_disaster(self) -> None:
        disaster = self._ask()
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
                disasters.to_csv(DISASTER, index=False)

                print()
                print(
                    f"{'+' * 60}"
                    f"\nREGISTERED\n\n"
                    f"Date Registered: {disaster['date_registered']}\n"
                    f"Disaster: {disaster['disaster_type']}\n"
                    f"Location: {disaster['location']}\n"
                    f"Severity: {disaster['severity']}\n"
                    f"{'+' * 60}"
                )
                print()
                time.sleep(5)

            else:
                disaster["ID"] = id
                disaster_df = pd.DataFrame([disaster])
                disaster_df.to_csv(DISASTER, index=False)

                print()
                print(
                    f"{'+' * 60}"
                    f"\nREGISTERED\n\n"
                    f"Date Registered: {disaster['date_registered']}\n"
                    f"Disaster: {disaster['disaster_type']}\n"
                    f"Location: {disaster['location']}\n"
                    f"Severity: {disaster['severity']}\n"
                    f"{'+' * 60}"
                )
                print()
                time.sleep(5)
        else:
            print()
            print(
                f"{'+' * 60}"
                f"\nALREADY REGISTERED\n\n"
                f"Date Registered: {disaster['date_registered']}\n"
                f"Disaster: {disaster['disaster_type']}\n"
                f"Location: {disaster['location']}\n"
                f"Severity: {disaster['severity']}\n"
                f"{'+' * 60}",
            )
            print()
            time.sleep(5)

    def update_disaster(self) -> None:
        register_disasters = self._read()

        self._show()
        print()
        selected_id = ask_loop("Enter which ID to update: ")
        print()
        print("Date will be auto-updated")
        print()

        if register_disasters:
            for rd in register_disasters:
                if str(rd.get("ID")).strip() == str(selected_id).strip():
                    dtype = ask_loop(f"Disaster Type: {rd['disaster_type']} => ")
                    location = ask_loop(f"Location: {rd['location']} => ")
                    severity = ask_loop(f"Severity: {rd['severity']} => ")
                    data = {
                        "date_registered": str(date.today()),
                        "disaster_type": dtype,
                        "location": location,
                        "severity": severity,
                    }

                    rd.update(data)
                    break

            disaster_df = pd.DataFrame(register_disasters)
            disaster_df.to_csv(DISASTER, index=False)

        else:
            print("Cannot update non-existing record")
            time.sleep(3)

    def delete_disaster(self) -> None:
        register_disaster = self._read()
        self._show()
        print()
        selected_id = ask_loop("Enter ID to delete: ", int)
        print()

        new = []
        _id = 1

        if register_disaster:
            for rd in register_disaster:
                if str(rd.get("ID")).strip() == str(selected_id).strip():
                    print(
                        f"{'+' * 60}"
                        f"\n  DELETED\n"
                        f"\n  ID: {rd['ID']}\n"
                        f"  Date: {rd['date_registered']}\n"
                        f"  Disaster: {rd['disaster_type']}\n"
                        f"  Location: {rd['location']}\n"
                        f"  Severity: {rd['severity']}\n"
                        f"{'+' * 60}"
                    )
                    del rd
                else:
                    rd["ID"] = _id
                    _id += 1
                    new.append(rd)
            disaster_df = pd.DataFrame(new)
            disaster_df.to_csv(DISASTER, index=False)

    def total_records(self) -> int | None:
        data = self._read()
        if data:
            return len(data)
        else:
            return None


class Resource:
    def __init__(self):
        self._id = 0

    def _read(
        self, operation: Literal["register", "show", "update", "delete"]
    ) -> dict | str | list | None:
        if operation == "register":
            try:
                data = pd.read_csv(RESOURCE, index_col=False)
                return data.to_dict(orient="list")
            except FileNotFoundError, pd.pandas.errors.EmptyDataError:
                return None
        elif operation == "show":
            try:
                return pd.read_csv(RESOURCE).to_string(index=False)
            except FileNotFoundError, pd.pandas.errors.EmptyDataError:
                return None
        else:
            try:
                data = pd.read_csv(RESOURCE, index_col=False)
                return data.to_dict(orient="records")
            except FileNotFoundError, pd.pandas.errors.EmptyDataError:
                return None

    def register_resource(self):
        resources = self._read(operation="register")

        self.show_resource()
        print()
        if isinstance(resources, dict):
            res_name = resources["name"]
            res_quant = resources["quantity"]
            res_id = resources["ID"]

            total_data = len(resources["name"])
            number_resources = int(
                input("Enter number of resources you want to append: ")
            )
            print("-" * 50)
            print()

            for id in range(number_resources):
                self._id = total_data + id + 1
                name = input(f"Enter Resource name numbered {self._id}: ")
                quant = int(input(f"Enter quantity of {name}: "))
                print("-" * 50)
                print()

                res_name.append(name)
                res_quant.append(quant)
                res_id.append(self._id)

            resources["ID"] = res_id
            resources["name"] = res_name
            resources["quantity"] = res_quant

        elif resources is None:
            resources = {}
            r_id = []
            r_name = []
            r_quant = []
            number_resources = int(input("Enter number of resources you want to add: "))

            for id in range(number_resources):
                self._id = self._id + 1
                res_name = input(f"Enter Resource name numbered {id + 1}: ")
                res_quant = int(input(f"Enter quantity of {res_name}: "))
                print("-" * 50)
                print()

                r_name.append(res_name)
                r_quant.append(res_quant)
                r_id.append(self._id)

            resources["ID"] = r_id
            resources["name"] = r_name
            resources["quantity"] = r_quant

        resource_df = pd.DataFrame(resources)
        resource_df.to_csv(RESOURCE, index=False)
        self.show_resource()
        time.sleep(5)

    def update_resource(self) -> None:
        reg_resource = self._read(operation="update")

        self.show_resource()
        print("-" * 40)
        print()
        selected_id = ask_loop("Enter which ID to update: ")
        print()

        if isinstance(reg_resource, list):
            for res in reg_resource:
                if str(res.get("ID")).strip() == str(selected_id).strip():
                    name = ask_loop(f"Name: {res['name']} => ")
                    quant = ask_loop(f"Quantity: {res['quantity']} => ")
                    resource = {"name": name, "quantity": quant}
                    res.update(resource)
                    break

            resource_df = pd.DataFrame(reg_resource)
            resource_df.to_csv(RESOURCE, index=False)
            print("-" * 40)
            self.show_resource()
            time.sleep(5)

        elif reg_resource is None:
            print("No resource found.\nAdd resource to update it.")
            time.sleep(3)

    def delete_resource(self) -> None:
        reg_resource = self._read(operation="delete")

        self.show_resource()
        print()
        selected_id = ask_loop("Enter ID to delete: ")
        print()

        new = []
        _id = 1

        if isinstance(reg_resource, list):
            for rr in reg_resource:
                if str(rr.get("ID")).strip() == str(selected_id).strip():
                    print(
                        f"{'+' * 60}"
                        f"DELETED\n"
                        f"ID: {rr['ID']}\n"
                        f"Name: {rr['name']}\n"
                        f"Quantity: {rr['quantity']}\n"
                        f"{'+' * 60}"
                    )
                    del rr
                    time.sleep(5)
                else:
                    rr["ID"] = str(_id).strip()
                    _id += 1
                    new.append(rr)

            disaster_df = pd.DataFrame(new)
            disaster_df.to_csv(RESOURCE, index=False)

    def show_resource(self):
        reg_resource = self._read(operation="show")
        print(reg_resource)


class Visuals:
    def _read(self, file: Literal["disasters", "resources"]) -> dict | list | None:
        if file == "disasters":
            try:
                data = pd.read_csv(DISASTER, index_col=False)
                return data.to_dict(orient="records")
            except FileNotFoundError, pd.pandas.errors.EmptyDataError:
                return None
        else:
            try:
                data = pd.read_csv(RESOURCE, index_col=False)
                return data.to_dict(orient="list")
            except FileNotFoundError, pd.pandas.errors.EmptyDataError:
                return None

    def disaster(self):
        self.SEVERITIES = ["Low", "Medium", "High", "Critical"]
        data = self._read(file="disasters")

        low = []
        med = []
        hig = []
        cri = []

        if data:
            for disaster in data:
                d_type = disaster["disaster_type"]
                location = disaster["location"]
                severity = disaster["severity"].lower()
                if severity == self.SEVERITIES[0].lower():
                    dis = {"type": d_type, "location": location}
                    low.append(dis)
                elif severity == self.SEVERITIES[1].lower():
                    dis = {"type": d_type, "location": location}
                    med.append(dis)
                elif severity == self.SEVERITIES[2].lower():
                    dis = {"type": d_type, "location": location}
                    hig.append(dis)
                elif severity == self.SEVERITIES[3].lower():
                    dis = {"type": d_type, "location": location}
                    cri.append(dis)

        total_number = [len(low), len(med), len(hig), len(cri)]

        graph.bar(self.SEVERITIES, total_number)
        graph.grid(True, axis="y")

        graph.xlabel("Severity")
        graph.ylabel("Total Number of Disaster Based on Severity")

        graph.title("Disaster Visualization Based on Severity")
        graph.show()

    def resource(self):
        _data = self._read(file="resources")

        if _data:
            names = _data["name"]
            quants = _data["quantity"]

            graph.bar(names, quants, color="skyblue")
            graph.xlabel("Available Resources")
            graph.ylabel("Quantities of Available Resources")
            graph.title("Resource Visualization")
            graph.show()


def main():
    resource = Resource()
    disaster = Disaster()
    visuals = Visuals()
    password = Password()

    if password.pass_loop():
        while True:
            tclean()
            header(title="Dashboard of DRMS", sub_title="DRMS")
            print(
                "What you want to do?\n\n"
                "1. Disaster Management\n"
                "2. Resource Management\n"
                "3. Visualize\n"
                "4. EXIT\n"
            )
            selected = ask_loop("What you want to access: ", int)
            if selected == 1:
                while True:
                    tclean()
                    header(title="Disaster Operations", sub_title="DRMS")
                    print(
                        "1. Register Disaster\n2. Update Disaster\n3. Delete Disaster\n4. BACK\n\n"
                    )
                    sub_disaster = ask_loop("Select: ", int)
                    if sub_disaster == 1:
                        tclean()
                        header(title="Register Disaster", sub_title="DRMS")
                        disaster.register_disaster()
                    elif sub_disaster == 2:
                        tclean()
                        header(title="Update Disaster", sub_title="DRMS")
                        disaster.update_disaster()
                    elif sub_disaster == 3:
                        tclean()
                        header(title="Delete Disaster", sub_title="DRMS")
                        disaster.delete_disaster()
                    elif sub_disaster == 4:
                        break
                    else:
                        print("Wrong Selection. Choose Again.\nChoose Between 1-4.")
                        time.sleep(1.5)

            elif selected == 2:
                while True:
                    tclean()
                    header(title="Resource Operations", sub_title="DRMS")
                    print(
                        "1. Register Resource\n2. Update Resource\n3. Delete Resource\n4. BACK\n"
                    )
                    sub_resource = ask_loop("Selected: ", int)
                    if sub_resource == 1:
                        tclean()
                        header(title="Resource Registration", sub_title="DRMS")
                        resource.register_resource()
                    elif sub_resource == 2:
                        tclean()
                        header(title="Resource Updation", sub_title="DRMS")
                        resource.update_resource()
                    elif sub_resource == 3:
                        tclean()
                        header(title="Resource Deletion", sub_title="DRMS")
                        resource.delete_resource()
                    elif sub_resource == 4:
                        break
                    else:
                        print("Wrong Selection. Choose Again.\nChoose Between 1-4.")
                        time.sleep(1.5)

            elif selected == 3:
                while True:
                    tclean()
                    header(
                        title="Visualization of Resources and Disasters",
                        sub_title="DRMS",
                    )
                    print("1. Disaster\n2. Resource\n3. BACK\n")
                    sub_visual = ask_loop("Select: ", int)
                    if sub_visual == 1:
                        visuals.disaster()
                    elif sub_visual == 2:
                        visuals.resource()
                    elif sub_visual == 3:
                        break
                    else:
                        print("Wrong Selection. Choose Again.\nChoose Between 1-3")
                        time.sleep(1.5)

            elif selected == 4:
                print("Exiting DRMS")
                time.sleep(0.5)
                exit()

            else:
                print("Wrong Selection. Choose Again.\nChoose Between 1-4")
                time.sleep(1.5)


if __name__ == "__main__":
    main()
