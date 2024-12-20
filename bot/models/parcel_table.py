import logging

from parcel_tw import TrackingInfo

from ..configs.platform_config import platform_to_id
from .db import Database


class ParcelTable:
    def __init__(self, db: Database):
        self.db = db

    def create_table(self):
        try:
            self.db.cursor.execute("""
            CREATE TABLE IF NOT EXISTS parcels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id TEXT NOT NULL,
                platform_id INTEGER NOT NULL,
                status TEXT NOT NULL,
                update_time TEXT NOT NULL,
                FOREIGN KEY (platform_id) REFERENCES platform (id)
                UNIQUE (order_id, platform_id)
            );
            """)
            self.db.conn.commit()
        except Exception as e:
            logging.error(f"Error creating table: {e}")
            raise RuntimeError("Error creating table")

    def insert(self, tracking_info: TrackingInfo):
        try:
            self.db.cursor.execute(
                """
            INSERT OR IGNORE INTO parcels (order_id, platform_id, status, update_time)
            VALUES (?, ?, ?, datetime('now', 'localtime'));
            """,
                (
                    tracking_info.order_id,
                    platform_to_id[tracking_info.platform],
                    tracking_info.status,
                ),
            )
            self.db.conn.commit()
        except Exception as e:
            logging.error(f"Error inserting data: {e}")
            raise RuntimeError("Error inserting parcel")

    def get(self, order_id, platform_id):
        try:
            self.db.cursor.execute(
                """
            SELECT * FROM parcels WHERE order_id = ? AND platform_id = ?;
            """,
                (order_id, platform_id),
            )
            return self.db.cursor.fetchone()
        except Exception as e:
            logging.error(f"Error getting data: {e}")
            raise RuntimeError("Error getting parcel")

    def get_status(self, order_id, platform_id):
        try:
            self.db.cursor.execute(
                """
            SELECT status FROM parcels WHERE order_id = ? AND platform_id = ?;""",
                (order_id, platform_id),
            )
            tuple = self.db.cursor.fetchone()
            return tuple[0] if tuple else None
        except Exception as e:
            logging.error(f"Error getting data: {e}")
            raise RuntimeError("Error getting parcel")

    def update(self, order_id, platform_id, status):
        try:
            self.db.cursor.execute(
                """
            UPDATE parcels SET status = ?, update_time = datetime('now')
            WHERE order_id = ? AND platform_id = ?;
            """,
                (status, order_id, platform_id),
            )
            # self.db.conn.commit()
        except Exception as e:
            logging.error(f"Error updating data: {e}")
            raise RuntimeError("Error updating parcel")

    def delete(self, order_id, platform_id):
        try:
            self.db.cursor.execute(
                """
            DELETE FROM parcels WHERE order_id = ? AND platform_id = ?;
            """,
                (order_id, platform_id),
            )
        except Exception as e:
            logging.error(f"Error deleting data: {e}")
            raise RuntimeError("Error deleting parcel")

    def query(self, limit, offset):
        try:
            self.db.cursor.execute(
                "SELECT * FROM parcels LIMIT ? OFFSET ?;", (limit, offset)
            )
            return self.db.cursor.fetchall()
        except Exception as e:
            logging.error(f"Error querying data: {e}")
            raise RuntimeError("Error querying parcel")
