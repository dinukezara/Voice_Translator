import csv
import os
import sqlite3
from datetime import datetime

from config import get_logger

logger = get_logger(__name__)


class Database:
    """
    SQLite database manager for storing translation history.
    """

    def __init__(self, db_path: str = "data/translations.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.create_table()

    def create_table(self) -> None:
        query = """
        CREATE TABLE IF NOT EXISTS translations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            source_lang TEXT NOT NULL,
            target_lang TEXT NOT NULL,
            original_text TEXT NOT NULL,
            translated_text TEXT NOT NULL
        )
        """
        self.conn.execute(query)
        self.conn.commit()
        logger.info("Database table ensured.")

    def insert(
        self,
        source_lang: str,
        target_lang: str,
        original_text: str,
        translated_text: str,
    ) -> None:
        query = """
        INSERT INTO translations (
            timestamp, source_lang, target_lang, original_text, translated_text
        ) VALUES (?, ?, ?, ?, ?)
        """
        self.conn.execute(
            query,
            (
                str(datetime.now()),
                source_lang,
                target_lang,
                original_text,
                translated_text,
            ),
        )
        self.conn.commit()
        logger.info("Translation saved to database.")

    def fetch_all(self) -> list:
        query = """
        SELECT id, timestamp, source_lang, target_lang, original_text, translated_text
        FROM translations
        ORDER BY id DESC
        """
        cursor = self.conn.execute(query)
        return cursor.fetchall()

    def export_csv(self, filename: str = "translations.csv") -> dict:
        try:
            rows = self.fetch_all()

            with open(filename, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(
                    [
                        "ID",
                        "Timestamp",
                        "Source Language",
                        "Target Language",
                        "Original Text",
                        "Translated Text",
                    ]
                )
                writer.writerows(rows)

            logger.info(f"CSV exported successfully: {filename}")
            return {"success": True, "filename": filename}

        except Exception as e:
            logger.exception("CSV export failed.")
            return {"success": False, "error": f"CSV export failed: {e}"}

    def close(self) -> None:
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed.")