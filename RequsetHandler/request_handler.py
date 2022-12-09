import sqlite3
from dataclasses import asdict

from DBTypes import Student, Attend, Schedule


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

    def insert_data(self, table_name: str, data: list):
        cursor = self.connection.cursor()

        try:
            for cur_data in data:
                dict_data = asdict(cur_data)
                cursor.execute(f'INSERT INTO {table_name}({", ".join(dict_data.keys())}) VALUES({", ".join("?" for _ in range(len(dict_data)))})', cur_data)
        except sqlite3.ProgrammingError:
            # add logging
            pass

        cursor.close()

    def update_db(self):
        pass

    def get_data(self):
        pass

    def is_connected(self) -> bool:
        return self.connection is not None
