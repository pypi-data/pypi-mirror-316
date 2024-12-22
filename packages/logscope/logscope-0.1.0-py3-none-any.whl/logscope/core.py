"""Core functionality for LogScope."""

import logging
from datetime import datetime
from typing import Callable
from logscope.handlers import SQLiteHandler
from logscope.formatter import LogScopeFormatter

def logger(
    db_path: str = 'logscope.db',
    style: str = 'colorful',
    name: str = None,
    level: int = logging.DEBUG
) -> Callable:
    """
    Create a logger with SQLite storage and pretty console output.
    
    Args:
        db_path: Path to SQLite database file
        style: Output style ('colorful' or 'plain')
        name: Optional logger name (defaults to timestamped name)
        level: Logging level (defaults to DEBUG)
        
    Returns:
        Logging function that takes arbitrary arguments
    """
    # Generate default name if none provided
    logger_name = name or f"LogScope_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Set up logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    logger.handlers = []  # Clear any existing handlers

    # Add SQLite handler
    sqlite_handler = SQLiteHandler(db_path)
    logger.addHandler(sqlite_handler)

    # Add console handler
    console_handler = logging.StreamHandler()
    console_formatter = LogScopeFormatter(style=style)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    def log(*args):
        logger.debug(" ".join(map(str, args)))

    return log