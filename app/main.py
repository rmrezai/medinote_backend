from fastapi import FastAPI
from pydantic import BaseModel
from app.hoop_engine import hoop_engine

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "MediNote API is live 🚀"}

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
