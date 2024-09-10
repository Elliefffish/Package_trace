import sqlite3
from pathlib import Path

current_dir = Path(__file__).parent
database_dir = current_dir.parent / "data"
database_dir.mkdir(parents=True, exist_ok=True)


class Database:
    def __init__(self, database_path: str | None = None):
        if database_path is None:
            database_path = database_dir / "database.db"

        self.conn = sqlite3.connect(database_path)
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        self.conn.close()
