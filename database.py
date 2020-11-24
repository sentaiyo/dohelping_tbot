import sqlite3
from sqlite3 import Error


class DataBase:
    def __init__(self, path):
        self.connection = None
        self.connect(path)

    @staticmethod
    def print_error(error):
        print(f"The error '{error}' occurred")

    def connect(self, path):
        try:
            self.connection = sqlite3.connect(path)
            print("Connection is successful")
        except Error as e:
            self.print_error(e)

    def execute_query(self, query):
        try:
            self.connection.cursor.execute(query)
            self.connection.commit()
            print("Query executed successfully")
        except Error as e:
            self.print_error(e)

    def execute_read_query(self, query):
        self.execute_query(query)
        return self.connection.cursor.fetchall()

    def create_table(self, table_name, *parameters):
        create_users_table_query = f"""
CREATE TABLE IF NOT EXISTS {table_name}(
    id INTEGER PRIMARY KEY AUTOINCREMENT"""
        for parameter in parameters:
            create_users_table_query += f""",
    {parameter['name']} {parameter['type']}"""
        create_users_table_query += """
);
"""
        self.execute_query(create_users_table_query)

    def insert(self, table_name, parameters, *strings):
        insert_query = f"""
INSERT INTO
    {table_name} {parameters}"""[:-2] + f""")
VALUES
    {strings[0]}"""[:-2] + ")"
        for string in strings[1::]:
            insert_query += f""",
    {string}"""[:-2] + ")"
        insert_query += ";"

        self.execute_query(insert_query)


class UsersData(DataBase):
    def __init__(self, path):
        self.connect(path)
        self.create_table('users', {'name': 'name', 'type': 'TEXT NOT NULL'})
