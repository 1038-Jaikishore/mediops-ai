import logging
import os
import json
from app.core.logging import setup_logging


def test_structured_json_logging():
    # Make sure logging is configured
    setup_logging()
    
    logger = logging.getLogger("app")
    test_message = "Structured logger verification event"
    test_metadata = "metadata-value-2026"
    
    # Emit a test log entry
    logger.info(test_message, extra={"test_key": test_metadata})
    
    # Find logs directory path relative to backend root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_file_path = os.path.join(base_dir, "logs", "app.log")
    
    # Assert log file was created
    assert os.path.exists(log_file_path)
    
    # Read the log file and verify the last line
    with open(log_file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    assert len(lines) > 0
    last_line = lines[-1].strip()
    
    # Parse log line as JSON
    parsed_log = json.loads(last_line)
    
    # Assert keys and values are correct
    assert "timestamp" in parsed_log
    assert parsed_log["level"] == "INFO"
    assert parsed_log["logger"] == "app"
    assert parsed_log["message"] == test_message
    assert parsed_log["test_key"] == test_metadata
