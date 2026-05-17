import logging
from pathlib import Path

from app.core.config import PROJECT_ROOT, settings


def resolve_log_path(log_file: str | Path) -> Path:
    log_path = Path(log_file)
    if log_path.is_absolute():
        return log_path
    return PROJECT_ROOT / log_path


def setup_logger(name: str, log_file: str | Path) -> logging.Logger:
    logger = logging.getLogger(name)

    level = getattr(logging, settings.log_level.upper(), logging.INFO)
    logger.setLevel(level)

    logger.handlers.clear()
    logger.propagate = False

    log_path = resolve_log_path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger