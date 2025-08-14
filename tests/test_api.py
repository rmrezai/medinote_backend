import json
import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from app.main import app

client = TestClient(app)


def load_sample_data():
    sample_path = ROOT / "data" / "patient_sample.json"
    with sample_path.open() as f:
        return json.load(f)


def test_generate_note_returns_expected_strings():
    data = load_sample_data()
    response = client.post("/generate-note", json=data)
    assert response.status_code == 200

    plan = response.json().get("assessment_plan", [])
    assert any("bacteremia" in item for item in plan)
    assert any("insulin glargine" in item for item in plan)
    assert any("POC Glucose readings" in item for item in plan)
