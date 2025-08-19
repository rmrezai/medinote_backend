import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from app.hoop_engine import hoop_engine
from app.note_generator import generate_assessment_plan


def load_sample_data():
    sample_path = ROOT / "data" / "patient_sample.json"
    with sample_path.open() as f:
        return json.load(f)


def test_hoop_engine_generates_assessment_plan(monkeypatch):
    data = load_sample_data()
    monkeypatch.setenv("NOTE_STRATEGY", "rule")
    result = hoop_engine(data)
    plan = result.get("assessment_plan", [])

    assert any("bacteremia" in item for item in plan)
    assert any("Recent labs" in item for item in plan)
    assert any("POC Glucose readings" in item for item in plan)


def test_note_generator_rule_based(monkeypatch):
    data = load_sample_data()
    monkeypatch.setenv("NOTE_STRATEGY", "rule")
    plan = generate_assessment_plan(data)

    assert any("bacteremia" in item for item in plan)
    assert any("Recent labs" in item for item in plan)
    assert any("POC Glucose readings" in item for item in plan)
