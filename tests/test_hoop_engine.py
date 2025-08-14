import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.hoop_engine import hoop_engine


def test_meal_percent_summary():
    data = {"meal_percent": [60, 40]}
    result = hoop_engine(data)
    assert any("Average meal intake" in line for line in result["assessment_plan"])
    assert any("50.0%" in line for line in result["assessment_plan"])
