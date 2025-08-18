import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_sample_data():
    sample_path = ROOT / "data" / "patient_sample.json"
    with sample_path.open() as f:
        return json.load(f)


def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "MediNote API is live 🚀"}


def test_generate_note_returns_expected_strings(client):
    data = load_sample_data()
    response = client.post("/generate-note", json=data)
    assert response.status_code == 200

    plan = response.json().get("assessment_plan", [])
    assert any("bacteremia" in item for item in plan)
    assert any("insulin glargine" in item for item in plan)
    assert any("POC Glucose readings" in item for item in plan)


def test_generate_note_with_minimal_data(client):
    response = client.post("/generate-note", json={})
    assert response.status_code == 200
    assert response.json()["assessment_plan"] == [
        "Plan: Continue current management, encourage healthy diet and exercise, follow up in 3 months."
    ]
