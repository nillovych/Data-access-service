from databases import PostgreDAO
from users import User, Admin, Moderator

admin = Admin('Salivan', 'Ichkins', 'sally.ich@outlook.com')
user = User('Stas', 'Checherry', 'same-stas-another-mail@outlook.com')
moderator = Moderator('Stepan', 'Bandera', 'sexy-boy@ukr.net')

postgre_admn = PostgreDAO(admin)

postgre_user = PostgreDAO(user)

postgre_moderator = PostgreDAO(moderator)

# postgre_moderator.create()

# postgre_user.create()
postgre_admn.create()

postgre_admn.delete()
