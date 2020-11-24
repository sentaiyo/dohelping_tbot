from database import UsersData


Data = UsersData("C:/Users/Admin/tables/table1.sqlite")
Data.insert('users', ('name',), ('Egor',), ('Masha',))
