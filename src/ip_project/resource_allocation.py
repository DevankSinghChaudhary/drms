from rich.console import Console

from ip_project.header import header
from ip_project.resource import Resource

console = Console()


def resource_allocation():
    header(title="Resource Allocation", sub_title="To Disaster Location")

    resource = Resource()

    resources = resource.load_resource(file="resources")
    disaster_meta = resource.load_resource(file="disaster_metadata")

    res_name = resources["name"]

    for disaster in disaster_meta:
        print(disaster["location"])


resource_allocation()
