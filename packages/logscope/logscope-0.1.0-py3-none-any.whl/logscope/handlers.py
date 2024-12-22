"""Custom logging handlers for LogScope."""

import sqlite3
import logging
import threading
from datetime import datetime
from logscope.utils import get_calling_details, format_timestamp_with_microseconds

class SQLiteHandler(logging.Handler):
    """Handler that writes log records to a SQLite database."""
    
    def __init__(self, db_path='logscope.db'):
        super().__init__()
        self.db_path = db_path
        self._local = threading.local()
        self.run_id = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

    def _get_connection(self):
        if not hasattr(self._local, 'connection'):
            self._local.connection = sqlite3.connect(self.db_path)
            self._local.cursor = self._local.connection.cursor()
            
            self._local.cursor.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run TEXT,
                    timestamp TEXT,
                    message TEXT,
                    filename TEXT,
                    lineno INTEGER,
                    source TEXT,
                    function TEXT
                )
            """)
            self._local.connection.commit()

        return self._local.connection, self._local.cursor

    def emit(self, record):
        connection, cursor = self._get_connection()

        timestamp = format_timestamp_with_microseconds(record) 
        source, function = get_calling_details(record)

        cursor.execute(
            "INSERT INTO logs (run, timestamp, message, filename, lineno, source, function) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                self.run_id,
                timestamp,
                record.getMessage(),
                record.pathname,
                record.lineno,
                source,
                function
            )
        )
        connection.commit()

    def close(self):
        if hasattr(self._local, 'connection'):
            self._local.connection.close()
        super().close()