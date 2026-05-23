import json

import pytest

from app.utils.io import load_text, save_json, load_csv

def test_load_text_success(tmp_path):
    file_path = tmp_path / "sample.txt"
    with file_path.open("w",encoding="utf-8") as f:
        f.write("hello ai")

    assert load_text(file_path) == "hello ai"

def test_save_json_success(tmp_path):
    file_path = tmp_path / "result.json"
    data = {"name": "AI Job Agent", "day": 4}
    save_json(data,file_path)
    with file_path.open("r",encoding="utf-8") as f:
        text = f.read()
    loaded = json.loads(text)

    assert loaded["name"] == "AI Job Agent"
    assert loaded["day"] == 4

def test_load_text_file_not_found(tmp_path):
    missing_path = tmp_path / "missing.txt"
    with pytest.raises(FileNotFoundError) as e:
        load_text(missing_path)
    assert "File not found" in str(e.value)

def test_load_csv_success(tmp_path):
    file_path = tmp_path / "jobs.csv"
    with file_path.open("w",encoding="utf-8") as f:
        f.write("company,title,jd_text\nDemo,AI Intern,Need Python\n")
    
    rows = load_csv(file_path)
    assert len(rows) == 1
    assert rows[0]["company"] == "Demo"