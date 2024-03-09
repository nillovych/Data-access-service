from abc import ABC, abstractmethod

import psycopg2

from conn_settings import POSTGRE_PARAMS  # parameters for connection to PostgreSQL
from users import AbstractUser


class DAO(ABC):
    def __init__(self, user: AbstractUser):
        user_data = user.__dict__
        permission_data = user.permission.__dict__
        user_data.pop('permission')

        self.columns_users, self.values_users = DAO._parser(user_data)
        self.columns_permissions, self.values_permissions = DAO._parser(permission_data)

        self.user_id = None

    @staticmethod
    def _parser(data):
        _columns = ', '.join(data.keys())
        _values = "', '".join(str(value) for value in data.values())
        return _columns, _values

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

                cursor.execute("INSERT INTO users ({}) VALUES ('{}');".format(self.columns_users, self.values_users))

                cursor.execute('SELECT LASTVAL()')
                self.user_id = cursor.fetchone()[0]

                cursor.execute(
                    "INSERT INTO permissions (user_id, {}) VALUES ({}, '{}');".format(self.columns_permissions,
                                                                                      self.user_id,
                                                                                      self.values_permissions))

                self.conn.commit()

        except psycopg2.Error as error:
            self.conn.rollback()
            print("Failed to insert data:", error)

    def delete(self):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE id = {};".format(self.user_id))

            self.conn.commit()

            self.conn.close()

        except psycopg2.Error as error:
            self.conn.rollback()
            print("Failed to delete user and associated permissions:", error)

    def update(self):
        pass
