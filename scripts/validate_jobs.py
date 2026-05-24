import json
import logging
import sys
from pathlib import Path

from pydantic import BaseModel, ValidationError

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from app.schemas.job import JobSchema, LLMExtractedJob  # noqa: E402


LOG_PATH = ROOT / "logs" / "day05_validate.log"
OUT_PATH = ROOT / "data" / "day05_validated_jobs.json"


def setup_logger() -> logging.Logger:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        filename=LOG_PATH,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        encoding="utf-8",
    )
    return logging.getLogger("day05_validate")


def validate_sample(
    name: str,
    model: type[BaseModel],
    data: dict,
    logger: logging.Logger,
) -> dict | None:
    try:
        obj = model.model_validate(data)
        logger.info("%s validate ok", name)
        return {"name": name, "data": obj.model_dump()}
    except ValidationError as exc:
        logger.warning("%s validate failed: %s", name, exc.errors())
        return None


def main() -> None:
    logger = setup_logger()

    samples: list[tuple[str, type[BaseModel], dict]] = [
        (
            "job_success",
            JobSchema,
            {
                "company": "OpenAI",
                "title": "AI Application Engineer",
                "skills": ["Python", "FastAPI", "Pydantic"],
            },
        ),
        (
            "job_fail_empty_title",
            JobSchema,
            {
                "company": "Example AI",
                "title": "   ",
                "skills": ["Python"],
            },
        ),
        (
            "llm_success",
            LLMExtractedJob,
            {
                "skills": ["Python", "RAG"],
                "degree": "本科及以上",
                "experience_years": 1,
                "location": "北京",
                "bonus_points": ["有 LLM 项目经验"],
            },
        ),
        (
            "llm_fail_empty_skills",
            LLMExtractedJob,
            {
                "skills": [],
                "degree": "硕士",
                "experience_years": 0,
                "location": "远程",
                "bonus_points": [],
            },
        ),
    ]

    results = []
    failed = 0

    for name, model, data in samples:
        result = validate_sample(name, model, data, logger)
        if result is None:
            failed += 1
        else:
            results.append(result)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"validated ok: {len(results)}, failed: {failed}")
    print(f"saved to: {OUT_PATH.relative_to(ROOT)}")
    print(f"log file: {LOG_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()