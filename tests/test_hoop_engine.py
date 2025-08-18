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


def test_hoop_engine_optional_sections():
    data = load_sample_data()
    result = hoop_engine(data, include_sections=["labs"])
    plan = result.get("assessment_plan", [])

    assert any("Recent labs" in item for item in plan)
    assert all("Vitals" not in item for item in plan)
    assert all("Patient presents with" not in item for item in plan)


def test_hoop_engine_custom_plan():
    data = load_sample_data()
    custom_plan = ["Plan: Start antibiotics."]
    result = hoop_engine(data, plan=custom_plan)
    plan = result.get("assessment_plan", [])

    assert custom_plan[0] in plan
    assert not any("Continue current management" in item for item in plan)
