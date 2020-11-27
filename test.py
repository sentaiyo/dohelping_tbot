from database import UsersData
from database import DataBase


Data = UsersData("C:/Users/Admin/tables/table1.sqlite")
Data.insert('users', ('name',), ('Egor',), ('Masha',))
Data.insert('short_tasks', ('task', 'user_id'), ('eat', '1'), ('play', '1'), ('eat', '2'), ('work', '2'))
Data0 = DataBase()
Data0.connect("C:/Users/Admin/tables/table1.sqlite")
print(Data0.select('users', '*'))
print(Data.select_join('users', 'short_tasks', 'user_id', 'task', 'name'))
