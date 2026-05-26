import pytest
from pydantic import ValidationError

from app.job_parser_core import parse_job_text


def test_parse_normal_job_text() -> None:
    text = """
    公司：星火智能
    岗位：AI应用开发实习生
    技能要求：Python、FastAPI、Pydantic、RAG
    经验要求：1年以上
    地点：北京
    """

    result = parse_job_text(text)

    assert result["company"] == "星火智能"
    assert result["title"] == "AI应用开发实习生"
    assert "Python" in result["skills"]
    assert "FastAPI" in result["skills"]
    assert result["experience_years"] == 1
    assert result["location"] == "北京"


def test_parse_empty_text_should_fail() -> None:
    with pytest.raises(ValueError, match="JD 文本不能为空"):
        parse_job_text("   ")


def test_parse_no_skills_should_fail() -> None:
    text = """
    公司：无技能公司
    岗位：后端实习生
    经验要求：1年以上
    地点：上海
    """

    with pytest.raises(ValidationError):
        parse_job_text(text)