import sqlite3
from sqlite3 import Error


class DataBase:
    def __init__(self, path=None):
        self.connection = None
        if path is not None:
            self.connect(path)

    @staticmethod
    def print_error(error, query):
        print(f"""The error '{error}' occurred in query:
{query}""")

    def connect(self, path):
        try:
            self.connection = sqlite3.connect(path)
        except Error as e:
            self.print_error(e, f"connect('{path}')")

    def execute_query(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
        except Error as e:
            self.print_error(e, query)

    def execute_read_query(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
            return cursor.fetchall()
        except Error as e:
            self.print_error(e, query)

    def create_table(self, table_name, foreign_keys_description=None, *parameters):
        create_table_query = f"""
CREATE TABLE IF NOT EXISTS {table_name}(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT"""
        for parameter in parameters:
            create_table_query += f""",
    {parameter}"""
        if foreign_keys_description is not None:
            create_table_query += f""",
    {foreign_keys_description}"""
        create_table_query += """
);
"""
        self.execute_query(create_table_query)

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

    def update(self, table_name, test_parameter, update_parameter1, *update_parameters):
        update_query = f"""
UPDATE
    {table_name}
SET
    {update_parameter1}'"""
        for update_parameter in update_parameters:
            update_query += f""",
    {update_parameter}'"""
        update_query += f"""
WHERE
    {test_parameter}'
"""

        self.execute_query(update_query)

    def delete(self, table_name, parameter, parameter_value):
        delete_query = f"""
DELETE FROM
    {table_name}
WHERE
    {parameter} = '{parameter_value}'
"""

        self.execute_query(delete_query)


class UsersData(DataBase):
    def __init__(self, path):
        super().__init__(path)
        self.create_users_table()
        self.create_tasks_table()
        self.create_times_table()

    def create_users_table(self):
        self.create_table('users', None)

    def create_tasks_table(self):
        self.create_table('tasks',
                          'FOREIGN KEY (user_id) REFERENCES users (id)',
                          'task TEXT NOT NULL',
                          'difficulty INTEGER NOT NULL',
                          'user_id INTEGER NOT NULL')

    def create_times_table(self):
        self.create_table('times',
                          'FOREIGN KEY (user_id) REFERENCES users (id)',
                          'time TEXT NOT NULL',
                          'user_id INTEGER NOT NULL')

    def add_user(self, user_id):
        self.insert('users', ('id',), (user_id,))

    def add_time(self, time, user_id):
        self.insert('times', ('time', 'user_id'), (time, user_id))

    def add_task(self, task, difficulty, user_id):
        self.insert('tasks', ('task', 'difficulty', 'user_id'), (task, difficulty, user_id))

    def get_tasks_for_user(self, user_id):
        tasks = self.select('tasks', 'task', 'user_id', 'difficulty')
        if tasks is None:
            tasks = []
        tasks_for_user1 = ''
        tasks_for_user2 = ''
        tasks_for_user3 = ''
        for task in tasks:
            if task[1] == user_id:
                if task[2] == 1:
                    tasks_for_user1 += f'\n{task[0]}\n' \
                                       f'простая задача\n'
                if task[2] == 2:
                    tasks_for_user2 += f'\n{task[0]}\n' \
                                       f'средняя задача\n'
                if task[2] == 3:
                    tasks_for_user3 += f'\n{task[0]}\n' \
                                       f'сложная задача\n'
        return tasks_for_user3 + tasks_for_user2 + tasks_for_user1

    def delete_task(self, task):
        self.delete('tasks', 'task', task)
