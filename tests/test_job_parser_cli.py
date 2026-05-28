import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from scripts.job_parser_cli import build_prompt, clean_text, main, parse_job, validate_job


def test_clean_text_removes_extra_spaces() -> None:
    text = "  公司：星火智能\n\n岗位：AI 应用开发  "
    assert clean_text(text) == "公司：星火智能 岗位：AI 应用开发"


def test_build_prompt_contains_jd_text() -> None:
    prompt = build_prompt("岗位：AI应用开发实习生")
    assert "只返回 JSON" in prompt
    assert "岗位：AI应用开发实习生" in prompt


def test_validate_job_success() -> None:
    data = {
        "company": "星火智能",
        "title": "AI应用开发实习生",
        "skills": ["Python", "FastAPI"],
        "degree": "本科及以上",
        "experience_years": 1,
        "location": "北京",
        "bonus_points": [],
    }
    result = validate_job(data)
    assert result["company"] == "星火智能"
    assert "Python" in result["skills"]


def test_validate_job_rejects_empty_skills() -> None:
    data = {
        "company": "星火智能",
        "title": "AI应用开发实习生",
        "skills": [],
    }
    with pytest.raises(ValidationError):
        validate_job(data)


def test_parse_job_writes_output_file(tmp_path: Path) -> None:
    input_path = tmp_path / "job.txt"
    output_path = tmp_path / "parsed.json"
    input_path.write_text("岗位：AI应用开发实习生\n技能：Python FastAPI", encoding="utf-8")

    result = parse_job(input_path, output_path)

    assert output_path.exists()
    saved = json.loads(output_path.read_text(encoding="utf-8"))
    assert saved["job"]["title"] == result["job"]["title"]
    assert saved["llm"]["is_mock"] is True


def test_parse_job_rejects_empty_file(tmp_path: Path) -> None:
    input_path = tmp_path / "empty.txt"
    output_path = tmp_path / "parsed.json"
    input_path.write_text("   \n", encoding="utf-8")

    with pytest.raises(ValueError, match="JD 文本不能为空"):
        parse_job(input_path, output_path)


def test_main_returns_zero_and_prints_result(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    input_path = tmp_path / "job.txt"
    output_path = tmp_path / "parsed.json"
    input_path.write_text("岗位：AI应用开发实习生\n技能：Python", encoding="utf-8")

    exit_code = main(["--input", str(input_path), "--output", str(output_path)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "parse ok" in captured.out
    assert output_path.exists()