from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pathlib import Path
from pydantic import BaseModel
from app.hoop_engine import hoop_engine

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "MediNote API is live 🚀"}


@app.get("/note", response_class=HTMLResponse)
def note_page() -> HTMLResponse:
    """Serve a simple page for generating notes."""
    html_path = Path(__file__).resolve().parent / "templates" / "note.html"
    return HTMLResponse(html_path.read_text())

class PatientData(BaseModel):
    POC_glucose: list = []
    active_meds: list = []
    meal_percent: list = []
    labs: dict = {}
    vitals: dict = {}
    problems: list = []
    ICD10: list = []

@app.post("/generate-note")
async def generate_note(data: PatientData):
    input_data = data.dict()
    return hoop_engine(input_data)
