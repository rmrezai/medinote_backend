import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.hoop_engine import hoop_engine


def test_meal_percent_in_assessment_plan():
    sample = {"meal_percent": [50, 100, 0]}
    result = hoop_engine(sample)
    assert any("average meal intake" in entry.lower() for entry in result["assessment_plan"])
