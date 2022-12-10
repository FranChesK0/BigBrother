import sqlite3
from dataclasses import asdict
from typing import Any

from RequestHandler.DBTypes import DBObjectBase


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

    def is_connected(self) -> bool:
        return self.connection is not None

    def insert_one(self, table_name: str,
                   obj: DBObjectBase,
                   *fields: str) -> None:
        """
        Insert one new record given from `obj` to the `table_name`.
        If `fields` is not empty, insert only given object fields.
        """

        self.insert_many(table_name, [obj], *fields)

    def insert_many(self, table_name: str,
                    objs: list[DBObjectBase],
                    *fields: str) -> None:
        """
        Insert records given from `objs` to the `table_name`.
        If `fields` is not empty, insert only given object fields.
        If `objs` is empty list, nothing happens.
        """

        if (len(objs) == 0):
            return

        cursor: sqlite3.Cursor = self.connection.cursor()

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

    def update(self, table_name: str,
               data: dict[str, Any],
               condition: str | None = None):
        """
        Update records in `table_name` satisfying `condition`.
        If `data` is empty dict, nothing happens.
        """

        if (len(data) == 0):
            return

        cursor: sqlite3.Cursor = self.connection.cursor()

        try:
            query: str = "UPDATE {} SET {} {}".format(
                table_name,
                ','.join(f"{field}={value}" for field, value in data.items()),
                f"WHERE {condition}" if condition else ""
            )
            cursor.execute(query)

        except sqlite3.ProgrammingError:
            # add logging
            pass

        finally:
            self.connection.commit()
            cursor.close()

    def select_one(self, table_name: str,
                   condition: str | None = None,
                   *fields: str) -> Any:
        """
        Selects first record from `table_name` satisfying the `condition`.
        If `fields` is not empty, select only given table fields.
        """

        r = self.select_all(table_name, condition, *fields)

        return r[0] if len(r) else None

    def select_all(self, table_name: str,
                   condition: str | None = None,
                   *fields: str) -> list[Any]:
        """
        Selects all records from `table_name` satisfying the `condition`.
        If `fields` is not empty, select only given table fields.
        """

        cursor: sqlite3.Cursor = self.connection.cursor()

        try:
            query: str = "SELECT {} FROM {} {}".format(
                ','.join(fields) if len(fields) else '*',
                table_name,
                f"WHERE {condition}" if condition else ""
            )
            cursor.execute(query)

            data: list[Any] = cursor.fetchall()

        except sqlite3.ProgrammingError:
            # add logging
            pass

        finally:
            return data

    def delete_all(self, table_name: str,
                   condition: str | None = None) -> None:
        """
        Delete all records from `table_name` satisfying the `condition`.
        If `condition` is `None` clear `table_name`.
        """

        cursor: sqlite3.Cursor = self.connection.cursor()

        try:
            query: str = "DELETE FROM {} {}".format(
                table_name,
                f"WHERE {condition}" if condition else ""
            )
            cursor.execute(query)

        except sqlite3.ProgrammingError:
            # add logging
            pass

        finally:
            self.connection.commit()
            cursor.close()
