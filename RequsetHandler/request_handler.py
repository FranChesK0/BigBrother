import sqlite3
from dataclasses import asdict
from typing import Any

from RequsetHandler.DBTypes import DBObjectBase


class RequestHandler:
    def __init__(self, db_path: str):
        self.connection: sqlite3.Connection | None = None
        self.__connect_db(db_path)

    def __del__(self):
        self.connection.close()

    def __connect_db(self, db_path: str) -> None:
        try:
            self.connection = sqlite3.connect(db_path)

        except sqlite3.ProgrammingError:
            # add logging
            pass

        finally:
            return


    def insert_one(self, table_name: str, obj: DBObjectBase, *fields: str):
        """
        Insert one new record given from `obj` to the `table_name`.
        If `fields` is not empty, insert only given object fields.
        """

        cursor = self.connection.cursor()

        try:
            obj_dict: dict[str] = asdict(obj)
            f: tuple[str] = fields if len(fields) else obj_dict.keys()

            data_tuple: tuple = tuple(obj_dict.get(field) for field in f)

            query: str = "INSERT INTO {}({}) VALUES({})".format(
                table_name,
                ','.join(f),
                ','.join(['?'] * len(f))
            )
            cursor.execute(query, data_tuple)

        except sqlite3.ProgrammingError:
            # add logging
            pass

        finally:
            self.connection.commit()
            cursor.close()

    def insert_many(self, table_name: str, objs: list[DBObjectBase], *fields: str):
        """
        Insert records given from `objs` to the `table_name`.
        If `fields` is not empty, insert only given object fields.
        """

        cursor = self.connection.cursor()

        try:
            f: tuple[str] = fields if len(fields) else asdict(objs[0]).keys()

            data_tuples: list[tuple] = []
            for obj in objs:
                obj_dict: dict[str] = asdict(obj)
                data_tuples.append(tuple(obj_dict.get(field) for field in f))

            query: str = "INSERT INTO {}({}) VALUES({})".format(
                table_name,
                ','.join(f),
                ','.join(['?'] * len(f))
            )
            cursor.executemany(query, data_tuples)

        except sqlite3.ProgrammingError:
            # add logging
            pass

        finally:
            self.connection.commit()
            cursor.close()


    def update(self, table_name: str, fields: list[str], data: list[DBObjectBase]):
        pass


    def select_one(self, table_name: str, condition: str, *fields: str) -> Any:
        """
        Selects one record from `table_name` satisfying the `condition`.
        If `fields` is not empty, select only given table fields.
        """

        cursor = self.connection.cursor()

        try:
            query: str = "SELECT {} FROM {} WHERE {}".format(
                ','.join(fields) if len(fields) else '*',
                table_name,
                condition
            )
            cursor.execute(query)

            data: Any = cursor.fetchone()

        except sqlite3.ProgrammingError:
            # add logging
            pass

        finally:
            return data

    def select_all(self, table_name: str, condition: str, *fields: str) -> list[Any]:
        """
        Selects all records from `table_name` satisfying the `condition`.
        If `fields` is not empty, select only given table fields.
        """

        cursor = self.connection.cursor()

        try:
            query: str = "SELECT {} FROM {} WHERE {}".format(
                ','.join(fields) if len(fields) else '*',
                table_name,
                condition
            )
            cursor.execute(query)

            data: list[Any] = cursor.fetchall()

        except sqlite3.ProgrammingError:
            # add logging
            pass

        finally:
            return data

    def is_connected(self) -> bool:
        return self.connection is not None
