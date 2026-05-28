import json

import pytest

from app.clients.llm_client import MockLLMClient

def test_mock_llm_generate_returns_json() -> None:
    client = MockLLMClient()
    response = client.generate("岗位：AI应用开发实习生")
    data = json.loads(response.text)
    assert data["company"] == "星火智能"
    assert "Python" in data["skills"]
    assert response.is_mock is True
    assert response.elapsed_ms >= 0

def test_mock_llm_rejects_empty_prompt() -> None:
    client = MockLLMClient()
    with pytest.raises(ValueError, match="prompt 不能为空"):
        client.generate(" ")