from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_parse_job_ok() -> None:
    response = client.post(
        "/jobs/parse",
        json={
            "jd_text": "公司：星火智能\n岗位：AI应用开发实习生\n技能：Python FastAPI Pydantic"
        },
    )

    data = response.json()

    assert response.status_code == 200
    assert data["job"]["company"]
    assert data["job"]["title"]
    assert data["job"]["skills"]


def test_parse_job_empty_text() -> None:
    response = client.post("/jobs/parse", json={"jd_text": "   "})

    assert response.status_code == 400
    assert "jd_text" in response.json()["detail"]