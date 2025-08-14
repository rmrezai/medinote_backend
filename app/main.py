from fastapi import FastAPI
from pydantic import BaseModel, Field
from app.hoop_engine import hoop_engine

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "MediNote API is live 🚀"}

class PatientData(BaseModel):
    POC_glucose: list = Field(default_factory=list)
    active_meds: list = Field(default_factory=list)
    meal_percent: list = Field(default_factory=list)
    labs: dict = Field(default_factory=dict)
    vitals: dict = Field(default_factory=dict)
    problems: list = Field(default_factory=list)
    ICD10: list = Field(default_factory=list)

@app.post("/generate-note")
async def generate_note(data: PatientData):
    input_data = data.dict()
    return hoop_engine(input_data)
