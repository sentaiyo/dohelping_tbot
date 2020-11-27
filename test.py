from database import UsersData


Data = UsersData("C:/Users/Admin/tables/table1.sqlite")
Data.insert('users', ('name',), ('Egor',), ('Masha',))
Data.insert('short_tasks', ('task', 'user_id'), ('eat', '1'), ('play', '1'), ('eat', '2'), ('work', '2'))
print(Data.select('users', '*'))
print(Data.select_join('users', 'short_tasks', 'user_id', 'task', 'name'))
