from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from app.utils.logger import setup_logger

BASE_DIR = Path(__file__).resolve().parents[2]
LOG_PATH = BASE_DIR/ " logs" / "day07_llm.logs"


@dataclass
class LLMResponse:
    text: str
    provider: str
    elapsed_ms: float
    is_mock: bool = True


class MockLLMClient:
    def __init__(self, provider:str = "mock") -> None:
        self.provider = provider
        self.logger = setup_logger("day07_llm", str(LOG_PATH))

    def generate(self, prompt: str) -> LLMResponse:
        if not prompt.strip():
            raise ValueError("prompt 不能为空")
        
        start = time.perf_counter()
        self.logger.info(
            "llm request | provider=%s | prompt_chars=%s",
            self.provider,
            len(prompt)
        )

        data = {
            "company": "星火智能",
            "title": "AI应用开发实习生",
            "skills": ["Python", "FastAPI", "Pydantic", "RAG", "Agent", "Git"],
            "degree": "本科及以上",
            "experience_years": 1,
            "location": "北京",
            "bonus_points": ["有项目作品集优先"],
        }
        text = json.dumps(data, ensure_ascii=False)
        elapsed_ms = (time.perf_counter() - start) * 1000
        self.logger.info(
            "llm response | provider=%s | response_chars=%s | elapsed_ms=%.2f",
            self.provider,
            len(text),
            elapsed_ms,
        )
        return LLMResponse(text=text, provider=self.provider, elapsed_ms=elapsed_ms)
    

def build_llm_client() -> MockLLMClient:
    api_key = os.getenv("LLM_API_KEY", "").strip()
    provider = "mock" if not api_key else "mock_api_key_present"
    return MockLLMClient(provider=provider)