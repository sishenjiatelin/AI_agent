from fastapi import FastAPI,Request,Response
import uuid
from schema import JOB_data, LLMExtractedJob
from utils import Extract_LabelContent
import json
from typing import Any
import inspect
import time


# data = {
#             "company": "星火智能",
#             "post": "AI应用开发实习生",
#             "skills": ["Python", "FastAPI", "Pydantic", "RAG", "Agent", "Git"],
#             "degree": "本科及以上",
#             "experience_years": 1,
#             "location": "北京",
#             "description": "有项目作品集优先"
#         }

app = FastAPI(title="hahaha")

@app.middleware("http")
async def Request_id(request: Request, call_next) -> Response:
    request.state.re_id = str(uuid.uuid4())
    response = await call_next(request)
    response.headers["X-Request-ID"] = request.state.re_id
    return response

@app.get("/test")
async def wait_time() -> str:
    print("wait start")
    return "6 sec past,end"



# @app.post("/paser/job")
# def validate_job(data: dict[str, Any]) -> dict[str, Any]:
#     basic = JOB_data(
#         company=data["company"],
#         post=data["post"],
#         skills=data["skills"],
#     )
#     detail = LLMExtractedJob(
#         degree=data.get("degree"),
#         experience_years=data.get("experience_years"),
#         location=data.get("location"),
#         description=data.get("description"),
#     )
#     result = basic.model_dump()
#     result.update(detail.model_dump())

#     return result

