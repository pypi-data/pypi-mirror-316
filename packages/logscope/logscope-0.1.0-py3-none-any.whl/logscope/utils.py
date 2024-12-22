"""Utility functions for LogScope."""

import time
import inspect
import logging
from typing import Tuple

def get_calling_details(record: logging.LogRecord) -> Tuple[str, str]:
    """
    Get the calling context details for a log record.
    
    Args:
        record: The log record to analyze
        
    Returns:
        Tuple of (source code context, function name)
    """
    frame = inspect.currentframe()
    while frame:
        frame = frame.f_back
        if frame and frame.f_lineno == record.lineno and frame.f_code.co_filename == record.pathname:
            frame = frame.f_back
            break
    if frame:
        frame_info = inspect.getframeinfo(frame)
        func_name = frame.f_code.co_name if frame.f_code.co_name != '<module>' else '<global>'
        return (
            frame_info.code_context[0].strip() if frame_info.code_context else "<unknown>",
            func_name
        )
    else:
        return ("<unknown>", "<unknown>")

def format_timestamp_with_microseconds(record: logging.LogRecord) -> str:
    """
    Format a timestamp with microsecond precision.
    
    Args:
        record: The log record containing the timestamp
        
    Returns:
        Formatted timestamp string
    """
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(record.created))
    microseconds = int((record.created % 1) * 1000000)
    return f"{timestamp}.{microseconds:06d}"