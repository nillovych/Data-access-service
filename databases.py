from abc import ABC, abstractmethod

import psycopg2

from conn_settings import POSTGRE_PARAMS  # parameters for connection to PostgreSQL
from users import AbstractUser


class DAO(ABC):

    @staticmethod
    def _parsing(data):
        _columns = ', '.join(data.keys())
        _values = data.values()
        _placeholders = ', '.join(['%s'] * len(data))

        return _columns, _values, _placeholders

    @abstractmethod
    def create(self, user: AbstractUser):
        pass

    @abstractmethod
    def update(self, user: AbstractUser, **kwargs: dict):
        pass

    @abstractmethod
    def delete(self, user: AbstractUser):
        pass


class PostgreDAO(DAO):
    def __init__(self):
        try:
            self.db_params = POSTGRE_PARAMS
            self.conn = psycopg2.connect(**self.db_params)

        except psycopg2.Error:
            print('Failed to connect to PostgreSQL:', psycopg2.Error)

    def create(self, user: AbstractUser):
        try:
            with self.conn.cursor() as cursor:
                permissions_data = user.permissions
                user_data = user.__dict__
                user_data.pop('permissions')

                columns_user, values_user, placeholders_user = DAO._parsing(user_data)
                columns_permissions, values_permissions, plcholders_permission = DAO._parsing(permissions_data)

                user_query = f"INSERT INTO users ({columns_user}) VALUES ({placeholders_user});"
                cursor.execute(user_query, tuple(user_data.values()))

                cursor.execute('SELECT LASTVAL()')
                user_id = cursor.fetchone()[0]
                setattr(user, 'id', user_id)

                permissions_query = f"INSERT INTO permissions (user_id, {columns_permissions}) VALUES (%s, {plcholders_permission});"
                cursor.execute(permissions_query, (user_id,) + tuple(values_permissions))

            self.conn.commit()

        except psycopg2.Error as error:
            self.conn.rollback()
            print("Failed to insert data:", error)

    def delete(self, user: AbstractUser):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE id = %s;", (user.id,))

            self.conn.commit()

        except psycopg2.Error as error:
            self.conn.rollback()
            print("Failed to delete user and associated permissions: ", error)

    def update(self, user: AbstractUser, **kwargs: dict):
        try:
            with self.conn.cursor() as cursor:
                for key, value in kwargs.items():
                    cursor.execute(f"UPDATE users SET {key} = %s WHERE id = %s;",
                                   (value, user.id))

            self.conn.commit()

        except psycopg2.Error as error:
            self.conn.rollback()
            print("Failed to upgrade user: ", error)






