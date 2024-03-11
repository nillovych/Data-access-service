import re
from abc import ABC, abstractmethod


class AbstractUser(ABC):
    def __init__(self, name: str, surname: str, email: str):
        self.name = name
        self.surname = surname
        self.email = AbstractUser.validate_email(email)
        self.permissions = {'write_permission': False,
                            'read_permission': False,
                            'delete_permission': False,
                            'post_permission': False,
                            'export_permission': False}
        self.set_permission()

    @staticmethod
    def validate_email(email) -> str:
        if re.match(r'[^@]+@[^@]+\.[^@]+', email):
            return email
        else:
            raise ValueError(f'Invalid email address: {email}')

    @abstractmethod
    def set_permission(self):
        pass


class User(AbstractUser):

    def set_permission(self):
        self.permissions['write_permission'] = True
        self.permissions['read_permission'] = True
        self.permissions['delete_permission'] = True


class Moderator(AbstractUser):
    def set_permission(self):
        self.permissions['write_permission'] = True
        self.permissions['read_permission'] = True
        self.permissions['delete_permission'] = True
        self.permissions['post_permission'] = True


class Admin(AbstractUser):
    def set_permission(self):
        self.permissions['write_permission'] = True
        self.permissions['read_permission'] = True
        self.permissions['delete_permission'] = True
        self.permissions['post_permission'] = True
        self.permissions['export_permission'] = True
