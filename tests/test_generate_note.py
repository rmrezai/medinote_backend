import json
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


def load_sample():
    data_path = Path(__file__).resolve().parents[1] / "data" / "patient_sample.json"
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)


def test_generate_note_endpoint_returns_plan():
    client = TestClient(app)
    sample = load_sample()

    response = client.post("/generate-note", json=sample)
    assert response.status_code == 200
    data = response.json()

    assessment_text = " ".join(data["assessment_plan"])
    for phrase in [
        "Patient presents with",
        "POC Glucose readings",
        "Plan: Continue current management",
    ]:
        assert phrase in assessment_text
