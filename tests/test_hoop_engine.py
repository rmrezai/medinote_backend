from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from app.hoop_engine import hoop_engine


def test_meal_percent_in_assessment_plan():
    data = {"meal_percent": [60, 40]}
    result = hoop_engine(data)
    assert "Meal intake: 60%, 40% (average 50.0%)." in result["assessment_plan"]
