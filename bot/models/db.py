import pathlib
import sqlite3

from ..configs.db_config import DATABASE_DIR, DATABASE_NAME

ROOT_DIR = pathlib.Path(__file__).parent.parent.parent


class Database:
    def __init__(self, database_path: str | None = None):
        if database_path is None:
            database_path = ROOT_DIR / DATABASE_DIR / DATABASE_NAME

        self.conn = sqlite3.connect(database_path)
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.close()

    def close(self):
        self.conn.close()
        self.conn.close()
