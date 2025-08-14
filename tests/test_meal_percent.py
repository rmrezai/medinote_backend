import json
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.hoop_engine import hoop_engine


def test_meal_percent_in_assessment_plan():
    with open('data/patient_sample.json') as f:
        sample_data = json.load(f)

    result = hoop_engine(sample_data)
    assert any('Average meal intake' in item for item in result['assessment_plan'])

