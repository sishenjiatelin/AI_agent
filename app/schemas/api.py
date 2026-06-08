from __future__ import annotations 
from typing import Any 
from pydantic import BaseModel, Field

class JobParseRequest(BaseModel):
    jd_text: str = Field(..., description="岗位 JD 原文")

class LLMInfo(BaseModel): 
    provider: str 
    is_mock: bool 
    elapsed_ms: float
    
class JobParseResponse(BaseModel): 
    job: dict[str, Any] 
    llm: LLMInfo 
    request_id: str

class ErrorBody(BaseModel): 
    error_code: str 
    message: str 
    detail: str 
    request_id: str

class ErrorResponse(BaseModel): 
    error: ErrorBody