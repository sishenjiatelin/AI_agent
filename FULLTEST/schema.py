from pydantic import ValidationError, ValidationInfo, BaseModel, Field, field_validator
from utils import Load_Text, Extract_LabelContent, Save_Json
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[0]
DATA = BASE / "before.txt"
JSON = BASE / "after.json"

class JOB_data(BaseModel):
    company: str = Field(..., min_length = 1)
    post: str = Field(..., min_length = 1)
    skills: list[str] = Field(..., min_length = 1)

    @field_validator("company","post")
    @classmethod
    def val_str(cls, value:str, info: ValidationInfo):
        if not isinstance(value, str):
            raise ValueError(f"{info.field_name} must be str!!")
        if not value:
            raise ValueError(f"{info.field_name} can't be NONE!!")
        return value

    @field_validator("skills")
    @classmethod
    def val_liststr(cls, value:list[str], info: ValidationInfo):
        for skill in value:
            if not isinstance(skill, str):
                raise ValueError(f"{info.field_name} list's element must be str!!")
            if not skill:
                raise ValueError(f"{info.field_name} can't be NONE!!")
        return value

class LLMExtractedJob(BaseModel):
    degree: str | None = None
    experience_years: int | None = Field(default=None, ge=0)
    location: str | None = None
    description: str

    @field_validator("degree","location", "description")
    @classmethod
    def val_str(cls, value:str, info: ValidationInfo):
        if not isinstance(value, str):
            raise ValueError(f"{info.field_name} must be str!!")
        if not value:
            raise ValueError(f"{info.field_name} can't be NONE!!")
        return value
    
