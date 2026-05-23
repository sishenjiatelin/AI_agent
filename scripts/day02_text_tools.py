import json
from pathlib import Path
import re

BASE_DIR = Path(__file__).resolve().parents[1]

INPUT = BASE_DIR / "data/sample_job.txt"
OUTPUT = BASE_DIR /"data/day02_result.json"

SKILLS = ["Python", "FastAPI", "RAG", "Agent", "SQL", "Docker", "LLM", "API"]


def clean_text(text: str) -> str:
    return " ".join(re.split(r"[\s，、,.。]+", text))

def count_words(text: str) -> int:
    return len(text.split())

def match_keywords(text: str, keywords: list[str]) -> tuple[list[str], list[str]]:
    lower_text = text.lower()
    matched = []
    missing = []

    for keyword in keywords:
        if keyword.lower() in lower_text:
            matched.append(keyword)
        else:
            missing.append(keyword)

    return matched, missing

def main() -> None:
    text = INPUT.read_text(encoding="utf-8")
    cleaned = clean_text(text)
    matched, missing = match_keywords(cleaned, SKILLS)

    result = {
        "word_count": count_words(cleaned),
        "matched_skills": matched,
        "missing_skills": missing,
    }

    OUTPUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()