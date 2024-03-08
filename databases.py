from abc import ABC, abstractmethod

from users import AbstractUser


class DAO(ABC):
    @abstractmethod
    def create(self, user: AbstractUser):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def delete(self):
        pass
