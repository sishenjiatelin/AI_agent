import json
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from app.clients.llm_client import build_llm_client
from app.schemas.job import JobSchema, LLMExtractedJob
from app.utils.io import load_text, save_json

BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = BASE_DIR / "data" / "sample_job.txt"
OUTPUT_PATH = BASE_DIR / "data" / "extracted_job_example.json"

def build_prompt(jd_text: str) -> str:
    return f"""
请从下面的岗位 JD 中抽取结构化信息。
只返回 JSON，不要解释。

字段：
company, title, skills, degree, experience_years, location, bonus_points

JD:
{jd_text}
""".strip()

def validate_job(data: dict[str, Any]) -> dict[str, Any]:
    basic = JobSchema(
        company=data["company"],
        title=data["title"],
        skills=data["skills"],
    )
    detail = LLMExtractedJob(
        skills=data["skills"],
        degree=data.get("degree"),
        experience_years=data.get("experience_years"),
        location=data.get("location"),
        bonus_points=data.get("bonus_points", []),
    )
    result = basic.model_dump()
    result.update(detail.model_dump())
    return result

def main() -> None:
    jd_text = load_text(INPUT_PATH)
    prompt = build_prompt(jd_text)

    client = build_llm_client()
    response = client.generate(prompt)
    try:
        raw_data = json.loads(response.text)
        job = validate_job(raw_data)
    except (json.JSONDecodeError, KeyError, ValidationError) as error:
        raise ValueError(f"LLM 返回结果不可用: {error}") from error
    output = {
        "job": job,
        "llm": {
            "provider": response.provider,
            "is_mock": response.is_mock,
            "elapsed_ms": round(response.elapsed_ms, 2),
        },
    }
    save_json(output, OUTPUT_PATH)
    print(f"saved to {OUTPUT_PATH}")
    print(f"provider={response.provider} elapsed_ms={response.elapsed_ms:.2f}")


if __name__ == "__main__":
    main()