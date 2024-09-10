import logging

from .db import Database


class SubscriptionTable:
    def __init__(self, db: Database):
        self.db = db

    def create_table(self):
        try:
            self.db.cursor.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                order_id TEXT NOT NULL,
                platform_id INTEGER NOT NULL,
                subscription_time TEXT NOT NULL,
                FOREIGN KEY (platform_id) REFERENCES platform (id)
                FOREIGN KEY (order_id) REFERENCES events (order_id)
                UNIQUE (user_id, order_id, platform_id)
            );
            """)
        except Exception as e:
            logging.error(f"Error creating table: {e}")
            raise RuntimeError("Error creating table")

    def insert(self, user_id: str, order_id: str, platform_id: int):
        try:
            self.db.cursor.execute(
                """
            INSERT INTO subscriptions (user_id, order_id, platform_id, subscription_time)
            VALUES (?, ?, ?, datetime('now', 'localtime'));
            """,
                (user_id, order_id, platform_id),
            )
            self.db.conn.commit()
        except Exception as e:
            logging.error(f"Error inserting data: {e}")
            raise RuntimeError("Error inserting subscription")

    def get(self, user_id: str, order_id: str, platform_id: int):
        try:
            self.db.cursor.execute(
                """
            SELECT * FROM subscriptions
            WHERE user_id = ? AND order_id = ? AND platform_id = ?;
            """,
                (user_id, order_id, platform_id),
            )
            return self.db.cursor.fetchone()
        except Exception as e:
            logging.error(f"Error getting data: {e}")
            raise RuntimeError("Error getting subscription")

    def get_all(self):
        try:
            self.db.cursor.execute("SELECT * FROM subscriptions;")
            return self.db.cursor.fetchall()
        except Exception as e:
            logging.error(f"Error getting data: {e}")
            raise RuntimeError("Error getting all subscriptions")

    def delete(self, order_id, platform_id):
        try:
            self.db.cursor.execute(
                "DELETE FROM subscriptions WHERE order_id = ? AND platform_id = ?;",
                (order_id, platform_id),
            )
            self.db.conn.commit()
        except Exception as e:
            logging.error(f"Error deleting data: {e}")
            raise RuntimeError("Error deleting subscription")
