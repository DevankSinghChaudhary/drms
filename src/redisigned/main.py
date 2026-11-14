import time

import pandas

DISASTER_CSV = "./disasters_metadata.csv"


class DRMS:
    def register_disaster(self):
        dis_type = input(
            "Enter Disaster Type (Earthquake, Flood, Landslide, Tsunami, etc): "
        )
        dis_location = input(f"Enter location of {dis_type} (city, state): ")
        dis_severity = input(
            f"Enter severity of {dis_type} in {dis_location} (Low, Medium, High, Critical): "
        )

        disaster = {
            "type": dis_type.lower(),
            "location": dis_location.lower(),
            "severity": dis_severity.lower(),
        }

        df = pandas.DataFrame(disaster).to_csv(DISASTER_CSV, index=False, header=True)


def main_menu():
    while True:
        print("=" * 190)
        print(
            "                                                                        Disaster Resource Management System"
        )
        print("=" * 190)
        print()

        time.sleep(0.25)
        print("1. Disaster Registration")
        time.sleep(0.25)
        print("2. Resource Management")
        time.sleep(0.25)
        print("3. EXIT")

        time.sleep(0.25)
        nav = int(input("\n\nEnter where you want to navigate: "))
        print()

        drms = DRMS()
        if nav == 1:
            drms.register_disaster()
            print("DISASTER REGISTRATION")

        elif nav == 2:
            # resource_management
            print("RESOURCE MANAGEMENT")
        elif nav == 3:
            # EXIT
            print("EXITING DRMS...")
            time.sleep(0.5)
            break


main_menu()
