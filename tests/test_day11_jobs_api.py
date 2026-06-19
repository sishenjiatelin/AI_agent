from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_job_ok() -> None:
    response = client.post(
        "/jobs",
        json={
            "company": "星火智能",
            "title": "AI应用开发实习生",
            "jd_text": "负责 FastAPI、RAG、Agent 应用开发",
            "skills": ["Python", "FastAPI", "RAG"],
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] >= 1
    assert data["company"] == "星火智能"
    assert "Python" in data["skills"]


def test_list_jobs_ok() -> None:
    response = client.get("/jobs")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_job_not_found() -> None:
    response = client.get("/jobs/999999")

    assert response.status_code == 404