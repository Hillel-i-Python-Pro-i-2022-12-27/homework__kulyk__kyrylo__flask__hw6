from application.services.db_connection import DBConnect


def create_table():
    with DBConnect() as connection:
        with connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS phones (
                    phone_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    contact_name TEXT NOT NULL,
                    phone_value INTEGER NOT NULL
                )
            """
            )
