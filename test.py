from database import UsersData


Data = UsersData("C:/Users/Admin/tables/table1.sqlite")
Data.insert('users', ('name',), ('Egor',), ('Masha',))
print(Data.select('users', '*'))
print(Data.select_join('users', 'short_tasks', 'user_id', 'task', 'name'))
