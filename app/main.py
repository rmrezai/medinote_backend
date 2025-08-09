from fastapi import FastAPI
from pydantic import BaseModel
from app.hoop_engine import hoop_engine

app = FastAPI()

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
    result = hoop_engine(input_data)

    problems = "\n".join([f"- {p}" for p in result['ICD10']])
    aps = "\n\n".join(result['assessment_plan'])

    note = f"""
📋 ICD-10 Problem List:
{problems}

🧠 HPI:
[Insert 2-sentence HPI here]

🧾 Assessment & Plan:
{aps}

🏠 Disposition:
[Insert disposition planning here]
"""
    return {"note": note.strip()}