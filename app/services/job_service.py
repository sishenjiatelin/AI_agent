import json

from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.job import Job, JobCreate, JobRead, JobUpdate


def to_job_read(job: Job) -> JobRead:
    return JobRead(
        id=job.id,
        company=job.company,
        title=job.title,
        jd_text=job.jd_text,
        skills=json.loads(job.skills_json),
        created_at=job.created_at,
    )


def create_job(session: Session, payload: JobCreate) -> JobRead:
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


def list_jobs(
    session: Session,
    keyword: str | None = None,
    skill: str | None = None,
    page: int = 1,
    page_size: int = 10,
) -> list[JobRead]:
    page = max(page, 1)
    page_size = min(max(page_size, 1), 50)

    statement = select(Job).order_by(Job.id)

    jobs = session.exec(statement).all()
    result: list[Job] = []

    for job in jobs:
        skills = json.loads(job.skills_json)
        keyword_ok = True
        skill_ok = True

        if keyword:
            text = f"{job.company} {job.title} {job.jd_text}".lower()
            keyword_ok = keyword.lower() in text

        if skill:
            skill_ok = any(skill.lower() in item.lower() for item in skills)

        if keyword_ok and skill_ok:
            result.append(job)

    start = (page - 1) * page_size
    end = start + page_size
    return [to_job_read(job) for job in result[start:end]]


def get_job_or_404(session: Session, job_id: int) -> Job:
    job = session.get(Job, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="岗位不存在")
    return job


def get_job(session: Session, job_id: int) -> JobRead:
    job = get_job_or_404(session, job_id)
    return to_job_read(job)


def update_job(session: Session, job_id: int, payload: JobUpdate) -> JobRead:
    job = get_job_or_404(session, job_id)
    data = payload.model_dump(exclude_unset=True)

    if "company" in data:
        job.company = data["company"]
    if "title" in data:
        job.title = data["title"]
    if "jd_text" in data:
        job.jd_text = data["jd_text"]
    if "skills" in data:
        job.skills_json = json.dumps(data["skills"], ensure_ascii=False)

    session.add(job)
    session.commit()
    session.refresh(job)
    return to_job_read(job)


def delete_job(session: Session, job_id: int) -> dict[str, int | bool]:
    job = get_job_or_404(session, job_id)
    session.delete(job)
    session.commit()
    return {"deleted": True, "id": job_id}