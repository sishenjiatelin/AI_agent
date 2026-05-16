from __future__ import annotations

import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
SAMPLE_JOB_PATH = DATA_DIR / "sample_job.txt"
RESULT_PATH = DATA_DIR / "day02_result.json"
DEFAULT_KEYWORDS: tuple[str, ...] = (
    "Python",
    "FastAPI",
    "RAG",
    "Agent",
    "SQL",
)


def clean_text(text: str) -> str:
    """简单的清洗数据，不保行"""

    return " ".join(text.split())


def count_words(text: str) -> int:
    """查字数，可改"""
    cleaned_text = clean_text(text)
    if not cleaned_text:
        return 0
    chinese_chars = re.findall(r"[\u4e00-\u9fff]", cleaned_text)
    english_tokens = re.findall(r"[A-Za-z0-9_+#.-]+", cleaned_text)
    return len(chinese_chars) + len(english_tokens)


def extract_keywords(text:str, keywords:list[str]) -> dict[str, list[str]]:
    """从文本中提取命中的技能词，并返回命中和未命中的结果。"""
    cleaned_text = clean_text(text)
    lower_text = cleaned_text.lower()

    matched_keywords: list[str] = []
    missing_keywords: list[str] = []

    for keyword in keywords:
        if keyword.lower() in lower_text:
            matched_keywords.append(keyword)
        else:
            missing_keywords.append(keyword)
    return {
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
    }


def analyze_job_text(text: str, keywords: list[str] | None = None) -> dict[str, object]:
    """分析岗位 JD，返回后续项目可以保存或传给 API 的结构化结果。"""
    if keywords is None:
        keywords = list(DEFAULT_KEYWORDS)

    cleaned_text = clean_text(text)
    keyword_result = extract_keywords(cleaned_text, keywords)

    return {
        "word_count": count_words(cleaned_text),
        "matched_keywords": keyword_result["matched_keywords"],
        "missing_keywords": keyword_result["missing_keywords"],
    }


def main() -> None:
    """读取样例 JD，分析结果，打印到终端，并写入 JSON 文件。"""
    if not SAMPLE_JOB_PATH.exists():
        raise FileNotFoundError(f"找不到输入文件：{SAMPLE_JOB_PATH}")
    raw_text = SAMPLE_JOB_PATH.read_text(encoding="utf-8")
    result = analyze_job_text(raw_text)

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    result_json = json.dumps(result, ensure_ascii=False, indent=2)
    print(result_json)

    RESULT_PATH.write_text(result_json + "\n", encoding="utf-8")
    print(f"\n分析结果已写入：{RESULT_PATH}")


if __name__ == "__main__":
    main()