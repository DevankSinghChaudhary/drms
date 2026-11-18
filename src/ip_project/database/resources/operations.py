import pandas as pd

RESOURCE = "./resources.csv"


class ResourceCsv:
    def _read(self):
        try:
            data = pd.read_csv(RESOURCE, index_col=None)
            return data.to_dict(orient="records")
        except FileNotFoundError:
            return False

    def _check_duplication(self):
        already_registered = self._read()

    def register_resource(self, data: dict):
        reg_resource = self._read()
