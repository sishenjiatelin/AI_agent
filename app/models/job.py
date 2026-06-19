from datetime import datetime, timezone

from pydantic import field_validator
from sqlmodel import Field, SQLModel

class JobCreate(SQLModel):
    company: str
    title: str
    jd_text: str
    skills: list[str]

    @field_validator("company", "title", "jd_text")
    @classmethod
    def text_not_empty(cls, value: str) -> str:
        text = value.strip()
        if not text:
            raise ValueError("字段不能为空")
        return text

    @field_validator("skills")
    @classmethod
    def skills_not_empty(cls, value: list[str]) -> list[str]:
        skills = [item.strip() for item in value if item.strip()]
        if not skills:
            raise ValueError("skills 至少需要 1 个有效技能")
        return skills
    
class Job(SQLModel, table=True):
    __tablename__ = "jobs"

    id: int | None = Field(default=None, primary_key=True)
    company: str
    title: str
    jd_text: str
    skills_json: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class JobRead(SQLModel):
    id: int
    company: str
    title: str
    jd_text: str
    skills: list[str]
    created_at: datetime