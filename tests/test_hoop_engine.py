import json
from pathlib import Path

from app.hoop_engine import hoop_engine


def load_sample():
    data_path = Path(__file__).resolve().parents[1] / "data" / "patient_sample.json"
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)


def test_hoop_engine_generates_assessment_plan():
    sample = load_sample()
    result = hoop_engine(sample)

    assert "assessment_plan" in result
    assessment_text = " ".join(result["assessment_plan"])

    for phrase in [
        "Patient presents with",
        "Current medications",
        "Plan: Continue current management",
    ]:
        assert phrase in assessment_text
