import logging
import logging.handlers
import sys
import os
import json
from datetime import datetime
from app.core.config import settings


class JSONFormatter(logging.Formatter):
    """
    Custom formatter that outputs log records as single-line JSON strings.
    """
    def format(self, record: logging.LogRecord) -> str:
        # Standard attributes
        log_record = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Include traceback details if an exception occurred
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        # Include custom fields passed through 'extra'
        standard_attrs = {
            'name', 'msg', 'args', 'levelname', 'levelno', 'pathname', 'filename',
            'module', 'exc_info', 'exc_text', 'stack_info', 'lineno', 'funcName',
            'created', 'msecs', 'relativeCreated', 'thread', 'threadName',
            'processName', 'process', 'asctime'
        }
        for key, value in record.__dict__.items():
            if key not in standard_attrs:
                # If value is already JSON serialized string (from previous phase simulator logs), 
                # try to load it so we don't double-serialize it as a nested string.
                if isinstance(value, str):
                    try:
                        log_record[key] = json.loads(value)
                    except json.JSONDecodeError:
                        log_record[key] = value
                else:
                    log_record[key] = value

        return json.dumps(log_record)


def setup_logging() -> None:
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    # Resolve logs directory path dynamically relative to the backend workspace root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # points to backend/app/
    backend_root = os.path.dirname(base_dir) # points to backend/
    logs_dir = os.path.join(backend_root, "logs")
    
    # Automatic creation of log directory
    os.makedirs(logs_dir, exist_ok=True)
    log_file_path = os.path.join(logs_dir, "app.log")

    # Define handlers
    stdout_handler = logging.StreamHandler(sys.stdout)
    file_handler = logging.handlers.RotatingFileHandler(
        filename=log_file_path,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=5,
        encoding="utf-8"
    )

    # Set JSONFormatter
    formatter = JSONFormatter()
    stdout_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove existing default handlers if any to prevent duplicates
    root_logger.handlers = []
    root_logger.addHandler(stdout_handler)
    root_logger.addHandler(file_handler)

    # Configure app logger
    logger = logging.getLogger("app")
    logger.info("Structured JSON Logging initialized successfully", extra={"log_file": log_file_path})
