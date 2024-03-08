import re
from abc import ABC


class AbstractUser(ABC):
    pass


class User(AbstractUser):
    def __init__(self, name: str, surname: str, email: str):
        self.name = name
        self.surname = surname
        self.permissions = {'message_write': True,
                            'message_change': True,
                            'message_delete': False,
                            'message_export': False}

        self.email = self._validate_email(email)

    def _validate_email(self, email):
        if re.match(r'[^@]+@[^@]+\.[^@]+', email):
            return email

        else:
            raise ValueError(f'Invalid email address: {email}')


class Moderator(User):
    def __init__(self, name: str, surname: str, permissions: dict):
        super().__init__(name, surname, permissions)

        self.permissions['message_delete'] = True


class Admin(Moderator):
    def __init__(self, name: str, surname: str, permissions: dict):
        super().__init__(name, surname, permissions)

        self.permissions['message_export'] = True

