import sqlite3

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


class DB:
    def _initialize_db(self) -> None:
        self.connection = sqlite3.connect("drms.db")
        self.cursor = self.connection.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS disasters (
                disaster_id INTEGER PRIMARY KEY AUTOINCREMENT,
                date_registered TEXT NOT NULL,
                disaster_type TEXT NOT NULL,
                location TEXT NOT NULL,
                severity TEXT NOT NULL,
                UNIQUE(disaster_type, location, date_registered)
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS resources (
                resource_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                UNIQUE(name)
            )
        """)

        self.connection.commit()

    def register_disaster(self, data: dict) -> None:
        self._initialize_db()

        try:
            date_registered = data["date_registered"]
            disaster_type = data["disaster_type"]
            location = data["location"]
            severity = data["severity"]

            self.cursor.execute(
                """
                INSERT INTO disasters
                    (date_registered, disaster_type, location, severity)
                VALUES (?, ?, ?, ?)
            """,
                (date_registered, disaster_type, location, severity),
            )

            self.connection.commit()

            console.print(
                Panel(
                    f"[green]Date Registered: {date_registered}\nDisaster: {disaster_type}\nLocation: {location}\nSeverity: {severity}[/green]",
                    title="Seccessfully Disaster Registered",
                    border_style="green",
                )
            )
        except KeyError:
            console.print("[red]Key Details for Disaster is Missing[/red]")

    def update_disaster(self, data: dict) -> None:
        self._initialize_db()

        try:
            date_registered = data["date_registered"]
            disaster_type = data["disaster_type"]
            location = data["location"]
            severity = data["severity"]

            self.cursor.execute(
                """
                INSERT INTO disasters
                    (date_registered, disaster_type, location, severity)
                VALUES (?, ?, ?, ?)
            """,
                (date_registered, disaster_type, location, severity),
            )

            self.connection.commit()

            console.print(
                Panel(
                    f"[green]Date Registered: {date_registered}\nDisaster: {disaster_type}\nLocation: {location}\nSeverity: {severity}[/green]",
                    title="Seccessfully Disaster Registered",
                    border_style="green",
                )
            )
        except KeyError:
            console.print("[red]Key Details for Disaster is Missing[/red]")

    def register_resource(self, data: dict):
        self._initialize_db()

        try:
            res_name = data["name"]
            res_quant = data["quantity"]

            values = list(zip(res_name, res_quant))

            self.cursor.executemany(
                """
                INSERT INTO resources (name, quantity)
                VALUES (?, ?)
            """,
                (values),
            )

            self.connection.commit()

            console.print("[green]Success: Added to Resource[/green]")
        except KeyError:
            console.print("[red]Details for Resource is Missing[/red]")

    def update_resource(self, data: dict):
        self._initialize_db()

        try:
            res_id = data["id"]
            res_name = data["name"]
            res_qaunt = data["quantity"]

            # values = list(zip(res_name, res_qaunt))

            self.cursor.execute(
                """
                UPDATE resources SET name = ?, quantity = ?
                WHERE resource_id = ?
            """,
                (res_name, res_qaunt, res_id),
            )

            self.connection.commit()

            console.print("[green]Sucess: Updated Resource[/green]")

        except KeyError:
            console.print("[red]Details for Resource is Missing[/red]")

    def show_resource(self):
        try:
            connection = sqlite3.connect("drms.db")
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()

            cursor.execute("""
                SELECT * FROM resources
            """)

            table = Table(
                title="Available Resources",
                style="cyan",
                title_justify="center",
                caption="You can allocate resources to disaster location",
            )
            table.add_column("ID", justify="right", style="yellow")
            table.add_column("Name", style="cyan")
            table.add_column("Quantity")

            for row in cursor:
                id = row["resource_id"]
                name_row = row["name"]
                quant_row = row["quantity"]
                table.add_row(str(id), name_row, str(quant_row))

            print()
            console.print(table)

        except sqlite3.OperationalError:
            console.print("[red]Add Resource First.[/red]")


db = DB()
db.show_resource()
db.update_resource(data={"id": 1, "name": "First Aid", "quantity": 999})
db.show_resource()
