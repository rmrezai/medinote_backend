import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from app.hoop_engine import hoop_engine


def load_sample_data():
    sample_path = ROOT / "data" / "patient_sample.json"
    with sample_path.open() as f:
        return json.load(f)


def test_hoop_engine_generates_assessment_plan():
    data = load_sample_data()
    result = hoop_engine(data)
    plan = result.get("assessment_plan", [])

    assert any("bacteremia" in item for item in plan)
    assert any("Recent labs" in item for item in plan)
    assert any("POC Glucose readings" in item for item in plan)


def test_hoop_engine_handles_missing_fields():
    result = hoop_engine({})
    assert result["assessment_plan"] == [
        "Plan: Continue current management, encourage healthy diet and exercise, follow up in 3 months."
    ]


def test_hoop_engine_handles_empty_lists():
    data = {
        "problems": [],
        "labs": {},
        "vitals": {},
        "active_meds": [],
        "POC_glucose": [],
    }
    result = hoop_engine(data)
    assert result["assessment_plan"] == [
        "Plan: Continue current management, encourage healthy diet and exercise, follow up in 3 months."
    ]
