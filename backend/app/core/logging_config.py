import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Final, TextIO

FILE_NAME: Final[str] = "app.log"
FILE_DIR: Final[str] = "./logs"
FILE_SIZE: Final[int] = 1024 * 1024  # 1MB per file
BACKUP_COUNT: Final[int] = 5  # keeps last 5 files = 5MB max
FORMAT: Final[str] = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

try:
    os.makedirs(FILE_DIR, exist_ok=True)
except OSError as e:
    raise SystemExit(f"Error creating directory '{FILE_DIR}': {e}")

file_path: str = os.path.join(FILE_DIR, FILE_NAME)
file_handler = RotatingFileHandler(
    filename=file_path,
    maxBytes=FILE_SIZE,
    backupCount=BACKUP_COUNT,
)
file_handler.setFormatter(logging.Formatter(FORMAT))

console_handler: logging.StreamHandler[TextIO] = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(FORMAT))

log_level: int = (
    logging.DEBUG
    if os.environ.get("DEBUG", "false").lower() == "true"
    else logging.INFO
)

logging.basicConfig(
    level=log_level,
    format=FORMAT,
    handlers=[file_handler, console_handler],
)
