# Day10 curl 调用记录

## 1. 启动服务

```bash
uvicorn app.main:app --reload

## 2. 健康检查
curl http://127.0.0.1:8000/health

预期结果：

{
  "status": "ok",
  "service": "ai-job-agent",
  "day": "day10"
}
3. 成功解析 JD
curl -X POST "http://127.0.0.1:8000/jobs/parse" \
  -H "Content-Type: application/json" \
  -d '{"jd_text":"公司：星火智能\n岗位：AI应用开发实习生\n技能：Python FastAPI Pydantic"}'

预期结果包含：

{
  "job": {},
  "llm": {},
  "request_id": "xxxx"
}
4. 空文本错误
curl -X POST "http://127.0.0.1:8000/jobs/parse" \
  -H "Content-Type: application/json" \
  -d '{"jd_text":" "}'

预期结果：

{
  "error": {
    "error_code": "EMPTY_JD_TEXT",
    "message": "jd_text 不能为空",
    "detail": "请传入一段岗位 JD 文本",
    "request_id": "xxxx"
  }
}
