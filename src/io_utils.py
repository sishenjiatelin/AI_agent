from pathlib import Path
import csv
import json
import logging
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def resolve_path(path: str | Path) -> Path:
    """把相对路径转换成基于项目根目录的绝对路径。"""
    file_path = Path(path)
    if file_path.is_absolute():
        return file_path
    return PROJECT_ROOT / file_path


def load_text(path: str | Path, encoding: str = "utf-8") -> str:
    """读取文本文件，返回字符串内容。"""
    file_path = resolve_path(path)
    return file_path.read_text(encoding=encoding)


def load_csv(path: str | Path, encoding: str = "utf-8") -> list[dict[str, str]]:
    """读取 CSV 文件，返回由字典组成的列表。"""
    file_path = resolve_path(path)
    with file_path.open("r", encoding=encoding, newline="") as f:
        reader = csv.DictReader(f)
        return [dict(row) for row in reader]
       


def save_json(data: Any, path: str | Path, encoding: str = "utf-8") -> None:
    """把 Python 数据保存成 JSON 文件。"""
    file_path = resolve_path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding=encoding) as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def setup_logger(name: str, log_file: str | Path) -> logging.Logger:
    """创建一个同时输出到终端和文件的 logger。"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    log_path = resolve_path(log_file)
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