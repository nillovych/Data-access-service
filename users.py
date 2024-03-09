import re
from abc import ABC, abstractmethod


class AbstractUser(ABC):
    def __init__(self, name: str, surname: str, email: str):
        self.name = name
        self.surname = surname
        self.email = AbstractUser._validate_email(email)
        self.permissions = {'write': False,
                            'read': False,
                            'delete': False,
                            'post': False,
                            'export': False}
        self._set_permission()

    @staticmethod
    def _validate_email(email) -> str:
        if re.match(r'[^@]+@[^@]+\.[^@]+', email):
            return email
        else:
            raise ValueError(f'Invalid email address: {email}')

    @abstractmethod
    def _set_permission(self):
        pass


class User(AbstractUser):

    def _set_permission(self):
        self.permissions['write'] = True
        self.permissions['read'] = True
        self.permissions['delete'] = True


class Moderator(AbstractUser):
    def _set_permission(self):
        self.permissions['write'] = True
        self.permissions['read'] = True
        self.permissions['delete'] = True
        self.permissions['post'] = True


class Admin(AbstractUser):
    def _set_permission(self):
        self.permissions['write'] = True
        self.permissions['read'] = True
        self.permissions['delete'] = True
        self.permissions['post'] = True
        self.permissions['export'] = True
