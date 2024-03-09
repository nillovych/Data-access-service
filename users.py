import re
from abc import ABC, abstractmethod

from permissions import UserPermission, ModeratorPermission, AdminPermission


class AbstractUser(ABC):
    def __init__(self, name: str, surname: str, email: str):
        self.name = name
        self.surname = surname
        self.email = AbstractUser._validate_email(email)
        self.permission = self._set_permission()

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
        return UserPermission()


class Moderator(AbstractUser):
    def _set_permission(self):
        return ModeratorPermission()


class Admin(AbstractUser):
    def _set_permission(self):
        return AdminPermission()
