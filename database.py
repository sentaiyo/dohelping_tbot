import sqlite3
from sqlite3 import Error


class DataBase:
    def __init__(self, path=None):
        self.connection = None
        if path is not None:
            self.connect(path)

    @staticmethod
    def print_error(error):
        print(f"The error '{error}' occurred")

    def connect(self, path):
        try:
            self.connection = sqlite3.connect(path)
        except Error as e:
            self.print_error(e)

    def execute_query(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
        except Error as e:
            self.print_error(e)

    def execute_read_query(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
            print("Query executed successfully")
            return cursor.fetchall()
        except Error as e:
            self.print_error(e)

    def create_table(self, table_name, *parameters):
        create_users_table_query = f"""
CREATE TABLE IF NOT EXISTS {table_name}(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT"""
        for parameter in parameters:
            create_users_table_query += f""",
    {parameter[0]} {parameter[1]}"""
        create_users_table_query += """
);
"""
        self.execute_query(create_users_table_query)

    def insert_one_parameter(self, table_name, parameter, string1, strings):
        insert_query = f"""
INSERT INTO
    {table_name} ({parameter})
VALUES
    ('{string1}')"""
        for string in strings:
            insert_query += f""",
    ('{string}')"""
        insert_query += ";"

        self.execute_query(insert_query)

    def insert(self, table_name, parameters, string1, *strings):
        if len(parameters) == 1:
            strings0 = ()
            for string in strings:
                strings0 += (string[0],)
            self.insert_one_parameter(table_name, parameters[0], string1[0], strings0)
        else:
            insert_query = f"""
INSERT INTO
    {table_name} {parameters}
VALUES
    {string1}"""
            for string in strings:
                insert_query += f""",
    {string}"""
            insert_query += ";"

            self.execute_query(insert_query)

    def select(self, table_name, parameter1, *parameters):
        select_query = f"""
SELECT
    {parameter1}"""
        for parameter in parameters:
            select_query += f""",
    {parameter}"""
        select_query += f"""
FROM
    {table_name}"""

        return self.execute_read_query(select_query)

    def select_join(self, table1_name, table2_name, table2_id_parameter, select_parameter1, *select_parameters):
        select_query = f"""
SELECT
    {select_parameter1}"""
        for select_parameter in select_parameters:
            select_query += f""",
    {select_parameter}"""
        select_query += f"""
FROM
    {table2_name}
    INNER JOIN {table1_name} ON {table1_name}.id = {table2_id_parameter}
"""

        return self.execute_read_query(select_query)


class UsersData(DataBase):
    def __init__(self, path):
        super().__init__(path)
        self.create_table('users', ['name', 'TEXT NOT NULL'])
        self.create_table('short_tasks', ['task', 'TEXT NOT NULL'], ['user_id', """INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)"""])
