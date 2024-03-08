from abc import ABC, abstractmethod

import psycopg2

from conn_settings import POSTGRE_PARAMS  # PARAMETERS FOR DB-CONNECTION
from users import AbstractUser


class DAO(ABC):
    def __init__(self, user: AbstractUser):
        data = user.__dict__
        self.permissions = user.permissions
        data.pop('permissions')

        self.columns_users = ', '.join(data.keys())
        self.values_users = "', '".join(str(value) for value in data.values())


    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def delete(self):
        pass


class PostgreDAO(DAO):
    def __init__(self, user: AbstractUser):
        super().__init__(user)

        try:
            self.db_params = POSTGRE_PARAMS
            self.conn = psycopg2.connect(**self.db_params)

        except psycopg2.Error:
            print('Failed to connect to PostgreSQL:', psycopg2.Error)

    def create(self):
        try:
            with self.conn.cursor() as cursor:

                cursor.execute(f"INSERT INTO users ({self.columns_users}) VALUES ('{self.values_users}');")

                user_id = cursor.lastrowid

                for column in self.permissions:

                    value = self.permissions[column]
                    cursor.execute(f"INSERT INTO permissions (user_id, {column}) VALUES ({user_id}, '{value}');")

                self.conn.commit()

        except psycopg2.Error as error:
            self.conn.rollback()
            print("Failed to insert data:", error)

    def delete(self):
        pass

    def update(self):
        pass

    def __del__(self):
        self.conn.close()
