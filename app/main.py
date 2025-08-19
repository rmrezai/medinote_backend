from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pathlib import Path
from pydantic import BaseModel
from typing import List, Optional

from app.hoop_engine import mediNote_hoop_engine as hoop_engine

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
    baseline_Cr: Optional[float] = None
    Cr: Optional[float] = None
    eGFR: Optional[float] = None
    MAP: Optional[float] = None
    RR: Optional[float] = None
    WBC: Optional[float] = None
    SpO2: List[float] = []
    O2_flow: Optional[str] = None
    CXR_date: Optional[str] = None
    Mg: Optional[float] = None
    glucose: List[float] = []
    HbA1c: Optional[float] = None

    class Config:
        extra = "allow"

@app.post("/generate-note")
async def generate_note(data: PatientData):
    input_data = data.dict()
    return hoop_engine(input_data)
