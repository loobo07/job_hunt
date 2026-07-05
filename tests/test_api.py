from fastapi.testclient import TestClient

from app.api.main import create_app
from app.storage.database import create_database, create_session_factory
from tests.fixtures import SAMPLE_PROFILE


def make_client():
    engine, session_factory = create_session_factory("sqlite+pysqlite:///:memory:")
    create_database(engine)
    app = create_app(session_factory=session_factory)
    return TestClient(app)


def test_profile_and_matching_api_flow():
    client = make_client()

    profile_response = client.post("/profiles", json=SAMPLE_PROFILE)
    assert profile_response.status_code == 201
    profile_id = profile_response.json()["id"]

    ingest_response = client.post(
        "/ingest/run",
        json={"sources": ["adzuna", "greenhouse"], "greenhouse_boards": ["acme"]},
    )
    assert ingest_response.status_code == 200
    assert ingest_response.json()["inserted"] == 2

    jobs_response = client.get("/jobs")
    assert jobs_response.status_code == 200
    assert len(jobs_response.json()) == 2

    matches_response = client.post("/matches/search", json={"profile_id": profile_id})
    assert matches_response.status_code == 200
    matches = matches_response.json()
    assert matches[0]["total_score"] > 0
    assert "score_components" in matches[0]

    explanation_response = client.post(f"/matches/{matches[0]['job_id']}/explain", json={"profile_id": profile_id})
    assert explanation_response.status_code == 200
    assert explanation_response.json()["matched_skills"]

    feedback_response = client.post(
        "/feedback",
        json={"job_id": matches[0]["job_id"], "status": "saved", "rating": 5},
    )
    assert feedback_response.status_code == 201
    assert feedback_response.json()["status"] == "saved"


def test_source_status_api_reports_configured_sources():
    client = make_client()

    response = client.get("/sources")

    assert response.status_code == 200
    assert {source["name"] for source in response.json()} == {"adzuna", "greenhouse"}
