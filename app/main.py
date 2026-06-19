from __future__ import annotations 
import json 
import uuid 
from pathlib import Path 
from typing import Any 
from fastapi import FastAPI 
from fastapi.responses import JSONResponse 
from pydantic import ValidationError 

from fastapi import Depends, HTTPException
from sqlmodel import Session, select

from app.db.session import create_db_and_tables, get_session
from app.models.job import Job, JobCreate, JobRead
from app.clients.llm_client import build_llm_client 
from app.schemas.api import JobParseRequest, JobParseResponse 
from app.schemas.job import JobSchema, LLMExtractedJob 
from app.utils.logger import setup_logger

BASE_DIR = Path(__file__).resolve().parents[1]
LOG_PATH = BASE_DIR / "logs" / "day10_api.log"
LOG_PATH.parent.mkdir(exist_ok=True)

logger = setup_logger("day10_api", str(LOG_PATH))

app = FastAPI(title="AI Job Agent API", version="0.1.0")

@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()


def new_request_id() -> str: 
    return uuid.uuid4().hex[:8]


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

def api_error( status_code: int, error_code: str, message: str, detail: str, request_id: str, ) -> JSONResponse: 
    return JSONResponse( 
        status_code=status_code, 
        content={ "error": {"error_code": error_code, 
                            "message": message, 
                            "detail": detail, 
                            "request_id": request_id, } }, )

@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "ai-job-agent",
        "day": "day10",
    }


@app.post("/jobs/parse", response_model=JobParseResponse) 
def parse_job(payload: JobParseRequest) -> JobParseResponse | JSONResponse: 
    request_id = new_request_id() 
    jd_text = clean_text(payload.jd_text) 
    if not jd_text: 
        logger.warning("jobs parse bad request | request_id=%s", request_id) 
        return api_error( 400, "EMPTY_JD_TEXT", "jd_text 不能为空", "请传入一段岗位 JD 文本", request_id, ) 
    client = build_llm_client() 
    response = client.generate(build_prompt(jd_text)) 
    try: 
        raw_data = json.loads(response.text) 
        job = validate_job(raw_data) 
    except (json.JSONDecodeError, KeyError, ValidationError) as exc: 
        logger.error("jobs parse failed | request_id=%s | error=%s", request_id, exc) 
        return api_error( 500, 
                         "JOB_PARSE_FAILED", 
                         "岗位解析失败", 
                         str(exc), 
                         request_id, ) 
    logger.info( "jobs parse ok | request_id=%s | company=%s | title=%s", request_id, job["company"], job["title"], ) 
    return JobParseResponse( job=job,
                             llm={"provider": response.provider,
                                "is_mock": response.is_mock, 
                                "elapsed_ms": round(response.elapsed_ms, 2), }, 
                            request_id=request_id, )

def to_job_read(job: Job) -> JobRead:
    return JobRead(
        id=job.id,
        company=job.company,
        title=job.title,
        jd_text=job.jd_text,
        skills=json.loads(job.skills_json),
        created_at=job.created_at,
    )


@app.post("/jobs", response_model=JobRead)
def create_job(payload: JobCreate, session: Session = Depends(get_session)) -> JobRead:
    job = Job(
        company=payload.company,
        title=payload.title,
        jd_text=payload.jd_text,
        skills_json=json.dumps(payload.skills, ensure_ascii=False),
    )
    session.add(job)
    session.commit()
    session.refresh(job)
    return to_job_read(job)


@app.get("/jobs", response_model=list[JobRead])
def list_jobs(session: Session = Depends(get_session)) -> list[JobRead]:
    jobs = session.exec(select(Job).order_by(Job.id)).all()
    return [to_job_read(job) for job in jobs]


@app.get("/jobs/{job_id}", response_model=JobRead)
def get_job(job_id: int, session: Session = Depends(get_session)) -> JobRead:
    job = session.get(Job, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="岗位不存在")
    return to_job_read(job)