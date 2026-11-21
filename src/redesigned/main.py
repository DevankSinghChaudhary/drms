import pandas as pd

DISASTER = "./disasters_metadata.csv"
RESOUECE = "./resources.csv"
PASSWORD = "ADK"


def header(title: str, sub_title: str) -> None:
    title_width = 50 - len([char for char in title]) - 5
    stitle_width = 50 - len([char for char in sub_title]) - 5

    print("=" * 50)
    print("|", title, " " * title_width, "|")
    print("|", sub_title, " " * stitle_width, "|")
    print("=" * 50)


class Password:
    def __init__(self):
        self.TOTAL_TRIES = 5

    def ask_password(self) -> str:
        while True:
            _password = input("Enter Password: ")
            if not _password:
                print("Password Cannot be empty!")
                print()
                continue
            else:
                return _password

    def check(self):
        while True:
            print(f"Total Tries: {self.TOTAL_TRIES}")
            while True:
                self.password = self.ask_password()
                if self.password == "":
                    print("Password cannot be empty!")
                    continue
                else:
                    break

            if self.password == PASSWORD:
                print("Welcome to DRMS")
                return True
            else:
                self.TOTAL_TRIES = self.TOTAL_TRIES - 1
                if self.TOTAL_TRIES == 0:
                    print("YOU ARE NOT AUTHORIZED PERSON.")
                    break

                else:
                    print("Wrong Password. Try Again.")
                    continue


class Disaster:
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
            del disaster_copy["ID"]
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
                disasters.to_csv(DISASTER, index=False)

                print(
                    f"{'+' * 60}"
                    f"\nDate Registered: {disaster['date_registered']}\n"
                    f"Disaster: {disaster['disaster_type']}\n"
                    f"Location: {disaster['location']}\n"
                    f"Severity: {disaster['severity']}\n"
                    f"{'+' * 60}"
                )

            else:
                disaster["ID"] = id
                disaster_df = pd.DataFrame([disaster])
                disaster_df.to_csv(DISASTER, index=False)

                print(
                    f"{'+' * 60}"
                    f"\nDate Registered: {disaster['date_registered']}\n"
                    f"Disaster: {disaster['disaster_type']}\n"
                    f"Location: {disaster['location']}\n"
                    f"Severity: {disaster['severity']}\n"
                    f"{'+' * 60}"
                )
        else:
            print(
                f"{'+' * 60}"
                f"\nALREADY REGISTERED\n\n"
                f"Date Registered: {disaster['date_registered']}\n"
                f"Disaster: {disaster['disaster_type']}\n"
                f"Location: {disaster['location']}\n"
                f"Severity: {disaster['severity']}\n"
                f"{'+' * 60}",
            )

    def update_disaster(self, id: str, data: dict) -> None:
        register_disasters = self._read()

        if register_disasters:
            for rd in register_disasters:
                if str(rd.get("ID")).strip() == str(id).strip():
                    rd.update(data)
                    break

            disaster_df = pd.DataFrame(register_disasters)
            disaster_df.to_csv(DISASTER, index=False)

        else:
            print("Cannot update non-existing record")

    def delete_disaster(self, id: str) -> None:
        register_disaster = self._read()

        new = []
        _id = 1

        if register_disaster:
            for rd in register_disaster:
                if str(rd.get("ID")).strip() == str(id).strip():
                    print(
                        f"{'+' * 60}"
                        f"\nID: {rd['ID']}\n"
                        f"Date: {rd['date_registered']}\n"
                        f"Disaster: {rd['disaster_type']}\n"
                        f"Location: {rd['location']}\n"
                        f"Severity: {rd['severity']}\n"
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
    def _read(self):
        pass
