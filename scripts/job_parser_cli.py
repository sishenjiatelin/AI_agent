from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from pydantic import ValidationError

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.clients.llm_client import build_llm_client  # noqa: E402
from app.schemas.job import JobSchema, LLMExtractedJob  # noqa: E402
from app.utils.io import load_text, save_json  # noqa: E402
from app.utils.logger import setup_logger  # noqa: E402

LOG_PATH = ROOT / "logs" / "day08_cli.log"


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

def parse_job(input_path: Path, output_path: Path) -> dict[str, Any]:
    logger = setup_logger("day08_cli", str(LOG_PATH))
    logger.info("start parse | input=%s | output=%s", input_path, output_path)

    jd_text = clean_text(load_text(input_path))
    if not jd_text:
        raise ValueError("JD 文本不能为空")

    client = build_llm_client()
    response = client.generate(build_prompt(jd_text))

    try:
        raw_data = json.loads(response.text)
        job = validate_job(raw_data)
    except (json.JSONDecodeError, KeyError, ValidationError) as exc:
        logger.error("parse failed | error=%s", exc)
        raise ValueError(f"LLM 返回结果不可用: {exc}") from exc

    output = {
        "job": job,
        "llm": {
            "provider": response.provider,
            "is_mock": response.is_mock,
            "elapsed_ms": round(response.elapsed_ms, 2),
        },
    }
    save_json(output, output_path)
    logger.info("parse ok | company=%s | title=%s", job["company"], job["title"])
    return output


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Day8 CLI 岗位解析器 v0.1")
    parser.add_argument("--input", required=True, help="输入 JD 文本文件路径")
    parser.add_argument("--output", required=True, help="输出 JSON 文件路径")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    try:
        result = parse_job(Path(args.input), Path(args.output))
    except Exception as exc:
        print(f"parse failed: {exc}", file=sys.stderr)
        return 1

    job = result["job"]
    print(f"parse ok: {job['company']} - {job['title']}")
    print(f"saved to: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
