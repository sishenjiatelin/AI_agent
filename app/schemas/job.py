from typing import Any
from pydantic import BaseModel, Field, field_validator, ValidationInfo


def _clean_text_list(values: list[Any], field_name: str) -> list[str]:
    cleaned: list[str] = []

    for value in values:
        if not isinstance(value, str):
            raise ValueError(f"{field_name} 只能包含字符串")

        text = value.strip()
        if text and text not in cleaned:
            cleaned.append(text)

    if not cleaned:
        raise ValueError(f"{field_name} 至少需要 1 个有效值")

    return cleaned




class JobSchema(BaseModel):
    company: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    skills: list[str] = Field(..., min_length=1)

    @field_validator("company", "title", mode="before")
    @classmethod
    def strip_required_text(cls, value: Any, info: ValidationInfo) -> str:
        field_name = info.field_name

        if not isinstance(value, str):
            raise ValueError(f"{field_name} 必须是字符串")

        text = value.strip()
        if not text:
            raise ValueError(f"{field_name} 不能为空")

        return text
    @field_validator("skills", mode="after")
    @classmethod
    def validate_skills(cls, values: list[str]) -> list[str]:
        return _clean_text_list(values, "skills")
    
class LLMExtractedJob(BaseModel):
    skills: list[str] = Field(..., min_length=1)
    degree: str | None = None
    experience_years: int | None = Field(default=None, ge=0)
    location: str | None = None
    bonus_points: list[str] = Field(default_factory=list)

    @field_validator("skills", mode="after")
    @classmethod
    def validate_skills(cls, values: list[Any]) -> list[str]:
        return _clean_text_list(values, "skills")