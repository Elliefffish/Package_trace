import logging

from .db import Database


class PlatformTable:
    def __init__(self, db: Database):
        self.db = db

    def create_table(self):
        try:
            self.db.cursor.execute("""
            CREATE TABLE IF NOT EXISTS platforms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            );
            """)
            self.db.conn.commit()
        except Exception as e:
            logging.error(f"Error creating table: {e}")
            raise RuntimeError("Error creating table")

    def insert(self, name):
        try:
            self.db.cursor.execute("INSERT OR IGNORE INTO platforms (name) VALUES (?);", (name,))
            self.db.conn.commit()
        except Exception as e:
            logging.error(f"Error inserting data: {e}")
            raise RuntimeError("Error inserting platform")

    def get(self, platform_id):
        try:
            self.db.cursor.execute("SELECT * FROM platforms WHERE id = ?;", (platform_id,))
            return self.db.cursor.fetchone()
        except Exception as e:
            logging.error(f"Error getting data: {e}")
            raise RuntimeError("Error getting platform")
