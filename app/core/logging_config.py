import logging
from logging.handlers import RotatingFileHandler

from app.core.config import LOG_DIR, LOG_LEVEL


def configure_logging() -> None:

    # Create log directory
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    # Set logging format
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # Get root logger
    root_logger = logging.getLogger()

    # Set logging level
    log_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    root_logger.setLevel(log_level)

    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
        handler.close()

    # File handler
    file_handler = RotatingFileHandler(
        filename=LOG_DIR / "application.log",
        maxBytes=5_000_000,
        backupCount=3,
        encoding="utf-8",
    )

    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    # # Console handler
    # console_handler = logging.StreamHandler()
    # console_handler.setLevel(log_level)
    # console_handler.setFormatter(formatter)

    # Add handlers
    root_logger.addHandler(file_handler)
    # root_logger.addHandler(console_handler)