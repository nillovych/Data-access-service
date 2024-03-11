from src.databases import PostgreDAO, MysqlDAO, CommonDAO
from src.users import User

# Create user instance
user = User(name='Persie', surname='Jackson', email='pers.jafdcffks@mail.com')

# Create DAO's instances
postgre_dao = PostgreDAO()
mysql_dao = MysqlDAO()
common_dao = CommonDAO()

# Create, update, delete user in MySQL
mysql_dao.create(user)
mysql_dao.update(user, name='Rico', surname='Miura')
mysql_dao.delete(user)

# Create, update, delete user in PostgreSQL
postgre_dao.create(user)
postgre_dao.update(user, name='Rico', surname='Miura')
postgre_dao.delete(user)

# Create, update, delete user in both databases
common_dao.create(user)
common_dao.update(user, name='Rico', surname='Miura')
common_dao.delete(user)
