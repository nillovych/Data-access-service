from databases import PostgreDAO
from users import User

dao = PostgreDAO()

user = User(name='Vasyl', surname='Porechelin', email='mails@mail.com')
# admin = Admin(name = 'Ivar', surname = 'Boneless', email = 'ivar.boneless@mail.com')

#dao.create(user)

#dao.update(user, name='Elvin', surname='Sobko')

#dao.delete(user)
