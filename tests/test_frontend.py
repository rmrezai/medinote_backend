import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from app.main import app

client = TestClient(app)


def test_note_page_contains_textarea_and_copy_button():
    response = client.get("/note")
    assert response.status_code == 200
    html = response.text
    assert "id=\"note\"" in html
    assert "copy-btn" in html
