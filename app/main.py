from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError

from app.clients.llm_client import build_llm_client
from app.schemas.job import JobSchema, LLMExtractedJob
from app.utils.logger import setup_logger

BASE_DIR = Path(__file__).resolve().parents[1]
LOG_PATH = BASE_DIR / "logs" / "day09_api.log"
LOG_PATH.parent.mkdir(exist_ok=True)

logger = setup_logger("day09_api", str(LOG_PATH))

app = FastAPI(title="AI Job Agent API", version="0.1.0")


class JobParseRequest(BaseModel):
    jd_text: str


def clean_text(text: str) -> str:
    return " ".join(text.split())


def build_prompt(jd_text: str) -> str:
    return f"""
请从下面岗位 JD 中抽取结构化信息。
只返回 JSON，不要解释。
字段：company, title, skills, degree, experience_years, location, bonus_points

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


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "ai-job-agent",
        "day": "day09",
    }


@app.post("/jobs/parse")
def parse_job(payload: JobParseRequest) -> dict[str, Any]:
    jd_text = clean_text(payload.jd_text)
    if not jd_text:
        raise HTTPException(status_code=400, detail="jd_text 不能为空")

    client = build_llm_client()
    response = client.generate(build_prompt(jd_text))

    try:
        raw_data = json.loads(response.text)
        job = validate_job(raw_data)
    except (json.JSONDecodeError, KeyError, ValidationError) as exc:
        logger.error("jobs parse failed | error=%s", exc)
        raise HTTPException(status_code=500, detail=f"解析失败: {exc}") from exc

    logger.info("jobs parse ok | company=%s | title=%s", job["company"], job["title"])

    return {
        "job": job,
        "llm": {
            "provider": response.provider,
            "is_mock": response.is_mock,
            "elapsed_ms": round(response.elapsed_ms, 2),
        },
    }