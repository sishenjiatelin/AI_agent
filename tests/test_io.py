import pytest

from app.utils.io import (
    FileReadError,
    JsonFormatError,
    load_json,
    load_text,
    save_json,
)


def test_load_text_success(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("Hello AI Agent", encoding="utf-8")

    result = load_text(file_path)

    assert result == "Hello AI Agent"


def test_save_and_load_json_success(tmp_path):
    file_path = tmp_path / "result.json"
    data = {
        "word_count": 10,
        "matched_keywords": ["Python", "FastAPI"],
    }

    save_json(data, file_path)
    result = load_json(file_path)

    assert result == data


def test_load_text_missing_file_raises_clear_error(tmp_path):
    missing_file = tmp_path / "missing.txt"

    with pytest.raises(FileReadError, match="文件不存在"):
        load_text(missing_file)


def test_load_json_bad_format_raises_error(tmp_path):
    bad_json = tmp_path / "bad.json"
    bad_json.write_text('{"name": "AI Agent"', encoding="utf-8")

    with pytest.raises(JsonFormatError, match="JSON 格式错误"):
        load_json(bad_json)