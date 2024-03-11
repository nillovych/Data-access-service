import copy
from abc import ABC, abstractmethod

import mysql.connector
import psycopg2

from conn_settings import POSTGRE_PARAMS, MYSQL_PARAMS  # parameters for connection to PostgreSQL, MySQL
from users import AbstractUser


class AbstractDAO(ABC):
    @abstractmethod
    def create(self, user: AbstractUser):
        pass

    @abstractmethod
    def update(self, user: AbstractUser, **kwargs: dict):
        pass

    @abstractmethod
    def delete(self, user: AbstractUser):
        pass


class CommonDAO(AbstractDAO):
    def __init__(self):
        __all_dao_classes = BaseDAO.__subclasses__()
        self.all_dao_instances = []
        for dao_class in __all_dao_classes:
            self.all_dao_instances.append(dao_class())

    def create(self, user: AbstractUser):
        for dao_instance in self.all_dao_instances:
            dao_instance.create(user)

    def update(self, user: AbstractUser, **kwargs: dict):
        for dao_instance in self.all_dao_instances:
            dao_instance.update(user, **kwargs)

    def delete(self, user: AbstractUser):
        for dao_instance in self.all_dao_instances:
            dao_instance.delete(user)


class BaseDAO(AbstractDAO):

    @staticmethod
    def parse(data):
        data.pop('permissions', None)
        data.pop('id', None)
        columns = ', '.join(data.keys())
        values = data.values()
        placeholders = ', '.join(['%s'] * len(data))

        return columns, values, placeholders

    def create(self, user: AbstractUser):
        with self.conn.cursor() as cursor:
            permissions_data = user.permissions
            user_data = copy.copy(user.__dict__)

            columns_user, values_user, placeholders_user = BaseDAO.parse(user_data)
            columns_permissions, values_permissions, plcholders_permission = BaseDAO.parse(permissions_data)

            user_query = f"INSERT INTO users ({columns_user}) VALUES ({placeholders_user});"
            cursor.execute(user_query, tuple(user_data.values()))

            cursor.execute(self.sql_query_last_id)
            user_id = cursor.fetchone()[0]
            setattr(user, 'id', user_id)

            permissions_query = f"INSERT INTO permissions (user_id, {columns_permissions}) VALUES (%s, {plcholders_permission});"
            cursor.execute(permissions_query, (user_id,) + tuple(values_permissions))

        self.conn.commit()

    def update(self, user: AbstractUser, **kwargs: dict):
        with self.conn.cursor() as cursor:
            for key, value in kwargs.items():
                cursor.execute(f"UPDATE users SET {key} = %s WHERE id = %s;",
                               (value, user.id))

        self.conn.commit()

    def delete(self, user: AbstractUser):
        with self.conn.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE id = %s;", (user.id,))

        self.conn.commit()


class PostgreDAO(BaseDAO):
    def __init__(self):
        try:
            self.db_params = POSTGRE_PARAMS
            self.conn = psycopg2.connect(**self.db_params)
        except psycopg2.Error as error:
            print('Failed to connect to PostgreSQL:', error)

    def create(self, user: AbstractUser):
        self.sql_query_last_id = 'SELECT LASTVAL()'
        try:
            super().create(user)
        except psycopg2.Error as error:
            self.conn.rollback()
            print("Failed to insert data into PostgreSQL-Database:", error)

    def update(self, user: AbstractUser, **kwargs: dict):
        try:
            super().update(user, **kwargs)
        except psycopg2.Error as error:
            self.conn.rollback()
            print("Failed to upgrade user in PostgreSQL-Database: ", error)

    def delete(self, user: AbstractUser):
        try:
            super().delete(user)
        except psycopg2.Error as error:
            self.conn.rollback()
            print("Failed to delete user and associated permissions from PostgreSQL-Database: ", error)


class MysqlDAO(BaseDAO):
    def __init__(self):
        try:
            self.db_params = MYSQL_PARAMS
            self.conn = mysql.connector.connect(**self.db_params)

        except mysql.connector.Error as error:
            self.conn.rollback()
            print('Failed to connect to MySQL:', error)

    def create(self, user: AbstractUser):
        self.sql_query_last_id = 'SELECT LAST_INSERT_ID()'
        try:
            super().create(user)
        except mysql.connector.Error as error:
            self.conn.rollback()
            print("Failed to insert data into MySQL-Database:", error)

    def update(self, user: AbstractUser, **kwargs: dict):
        try:
            super().update(user, **kwargs)
        except mysql.connector.Error as error:
            self.conn.rollback()
            print("Failed to upgrade user in MySQL-Database: ", error)

    def delete(self, user: AbstractUser):
        try:
            super().delete(user)
        except mysql.connector.Error as error:
            self.conn.rollback()
            print("Failed to delete user and associated permissions from MySQL-Database: ", error)
