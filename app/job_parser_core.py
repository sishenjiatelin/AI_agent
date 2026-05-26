from pathlib import Path
import re
from typing import Any

from pydantic import ValidationError

from app.schemas.job import JobSchema, LLMExtractedJob
from app.utils.io import load_text, save_json
from app.utils.logger import setup_logger

BASE_DIR = Path(__file__).resolve().parents[1]
SAMPLE_PATH = BASE_DIR / "data" / "sample_job.txt"
OUTPUT_PATH = BASE_DIR / "data" / "parsed_job.json"
LOG_PATH = BASE_DIR / "logs" / "day06_parse.log"

KNOWN_SKILLS = [
    "Python",
    "FastAPI",
    "Pydantic",
    "SQL",
    "SQLite",
    "RAG",
    "LLM",
    "Agent",
    "Git",
]


def _find_labeled_value(text: str, labels: list[str]) -> str | None:
    for label in labels:
        pattern = rf"{label}\s*[:：]\s*(.+)"
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
    return None

def _extract_skills(text: str) -> list[str]:
    lower_text = text.lower()
    found: list[str] = []
    for skill in KNOWN_SKILLS:
        if skill.lower() in lower_text and skill not in found:
            found.append(skill)
    return found

def _extract_experience_years(text:str) -> int | None:
    match = re.search(r"(\d+)\s*[年|years?|Years?|YEARS?]", text)
    if match:
        return int(match.group(1))
    return None

def parse_job_text(text: str) -> dict[str, Any]:
    if not text.strip():
        raise ValueError("JD 文本不能为空")
    
    company = _find_labeled_value(text, ["公司", "公司名称"]) or "Mock公司"
    title = _find_labeled_value(text, ["岗位", "职位", "岗位名称"]) or "Mock岗位"
    skills = _extract_skills(text)
     
    basic_job = JobSchema(company=company, title=title, skills=skills)
    extracted = LLMExtractedJob(
        skills=skills,
        degree=_find_labeled_value(text, ["学历", "学历要求"]),
        experience_years=_extract_experience_years(text),
        location=_find_labeled_value(text, ["地点", "工作地点"]),
        bonus_points=[],
    )
    result = basic_job.model_dump()
    result.update(
        {
            "experience_years": extracted.experience_years,
            "degree": extracted.degree,
            "location": extracted.location,
            "bonus_points": extracted.bonus_points,
        }
    )
    return result

def parse_job_file(
    input_path: Path = SAMPLE_PATH,
    output_path: Path = OUTPUT_PATH,
) -> dict[str, Any]:
    logger = setup_logger("day06_parser", str(LOG_PATH))
    text = load_text(input_path)

    try:
        parsed = parse_job_text(text)
    except (ValueError, ValidationError) as error:
        logger.error("parse job failed: %s", error)
        raise

    save_json(parsed, output_path)
    logger.info("parse job success: %s - %s", parsed["company"], parsed["title"])
    return parsed

if __name__ == "__main__":
    result = parse_job_file()
    print(result)