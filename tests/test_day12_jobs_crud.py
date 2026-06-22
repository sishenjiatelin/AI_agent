from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def create_sample_job() -> int:
    response = client.post(
        "/jobs",
        json={
            "company": "星火智能",
            "title": "AI 应用开发实习生",
            "jd_text": "负责 Python、FastAPI、RAG 应用开发",
            "skills": ["Python", "FastAPI", "RAG"],
        },
    )
    assert response.status_code == 200
    return response.json()["id"]


def test_update_job_ok() -> None:
    job_id = create_sample_job()

    response = client.put(
        f"/jobs/{job_id}",
        json={
            "title": "LLM 应用开发实习生",
            "skills": ["Python", "FastAPI", "Agent"],
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "LLM 应用开发实习生"
    assert "Agent" in data["skills"]


def test_search_jobs_by_keyword() -> None:
    create_sample_job()

    response = client.get("/jobs?keyword=应用开发")

    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert "应用开发" in data[0]["jd_text"] or "应用开发" in data[0]["title"]


def test_search_jobs_by_skill() -> None:
    create_sample_job()

    response = client.get("/jobs?skill=FastAPI&page=1&page_size=5")

    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1

    assert any(
        "fastapi" in [skill.lower() for skill in job["skills"]]
        for job in data
    )


def test_delete_job_ok() -> None:
    job_id = create_sample_job()

    delete_response = client.delete(f"/jobs/{job_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["deleted"] is True

    get_response = client.get(f"/jobs/{job_id}")
    assert get_response.status_code == 404