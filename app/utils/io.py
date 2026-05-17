import csv
import json
import logging
from pathlib import Path
from typing import Any

from app.core.config import PROJECT_ROOT


logger = logging.getLogger(__name__)


class FileReadError(Exception):
    """读取文件失败时抛出的自定义异常。"""


class FileWriteError(Exception):
    """写入文件失败时抛出的自定义异常。"""


class JsonFormatError(Exception):
    """JSON 格式错误时抛出的自定义异常。"""


def resolve_path(path: str | Path) -> Path:
    file_path = Path(path)
    if file_path.is_absolute():
        return file_path
    return PROJECT_ROOT / file_path


def load_text(path: str | Path, encoding: str = "utf-8") -> str:
    file_path = resolve_path(path)

    if not file_path.exists():
        raise FileReadError(f"文件不存在：{file_path}")

    try:
        return file_path.read_text(encoding=encoding)
    except UnicodeDecodeError as exc:
        logger.exception("读取文本失败，编码错误：%s", file_path)
        raise FileReadError(f"文件编码错误，无法用 {encoding} 读取：{file_path}") from exc
    except OSError as exc:
        logger.exception("读取文本失败：%s", file_path)
        raise FileReadError(f"读取文件失败：{file_path}") from exc


def load_json(path: str | Path, encoding: str = "utf-8") -> Any:
    file_path = resolve_path(path)

    if not file_path.exists():
        raise FileReadError(f"JSON 文件不存在：{file_path}")

    try:
        with file_path.open("r", encoding=encoding) as f:
            return json.load(f)
    except json.JSONDecodeError as exc:
        logger.exception("JSON 格式错误：%s", file_path)
        raise JsonFormatError(f"JSON 格式错误：{file_path}") from exc
    except OSError as exc:
        logger.exception("读取 JSON 失败：%s", file_path)
        raise FileReadError(f"读取 JSON 失败：{file_path}") from exc


def save_json(data: Any, path: str | Path, encoding: str = "utf-8") -> None:
    file_path = resolve_path(path)

    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open("w", encoding=encoding) as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError as exc:
        logger.exception("写入 JSON 失败：%s", file_path)
        raise FileWriteError(f"写入 JSON 失败：{file_path}") from exc


def load_csv(path: str | Path, encoding: str = "utf-8") -> list[dict[str, str]]:
    file_path = resolve_path(path)

    if not file_path.exists():
        raise FileReadError(f"CSV 文件不存在：{file_path}")

    try:
        with file_path.open("r", encoding=encoding, newline="") as f:
            reader = csv.DictReader(f)
            return [dict(row) for row in reader]
    except OSError as exc:
        logger.exception("读取 CSV 失败：%s", file_path)
        raise FileReadError(f"读取 CSV 失败：{file_path}") from exc