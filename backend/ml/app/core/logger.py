import atexit
import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_FILE = Path(os.getenv("LOG_FILE", "logs/app.log"))
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
FORMATTER = logging.Formatter(LOG_FORMAT)

root_logger = logging.getLogger()
root_logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

has_stdout_handler = any(
    isinstance(handler, logging.StreamHandler)
    and not isinstance(handler, logging.FileHandler)
    for handler in root_logger.handlers
)
if not has_stdout_handler:
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(FORMATTER)
    root_logger.addHandler(stdout_handler)

log_file = str(LOG_FILE.resolve())
has_file_handler = any(
    isinstance(handler, logging.FileHandler)
    and Path(handler.baseFilename) == Path(log_file)
    for handler in root_logger.handlers
)
if not has_file_handler:
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=int(os.getenv("LOG_MAX_BYTES", "10485760")),
        backupCount=int(os.getenv("LOG_BACKUP_COUNT", "5")),
    )
    file_handler.setFormatter(FORMATTER)
    root_logger.addHandler(file_handler)

atexit.register(logging.shutdown)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
