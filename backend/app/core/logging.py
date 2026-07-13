import logging
import sys
from typing import Any, Dict
from app.core.config import settings


def setup_logging() -> None:
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    # Basic logging config
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    # Suppress verbose logs from third-party libraries if needed
    logging.getLogger("uvicorn.access").handlers = []
    
    logger = logging.getLogger("app")
    logger.info("Logging configured with level: %s", settings.LOG_LEVEL)
