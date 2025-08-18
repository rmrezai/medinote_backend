from fastapi import FastAPI
from pydantic import BaseModel, Field, confloat
from app.hoop_engine import hoop_engine

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "MediNote API is live 🚀"}

class PatientData(BaseModel):
    POC_glucose: list[confloat(gt=0)] = Field(
        default_factory=list,
        description="Point-of-care glucose readings in mg/dL. Values must be greater than 0.",
    )
    active_meds: list[str] = Field(
        default_factory=list, description="List of current medications."
    )
    meal_percent: list[confloat(ge=0, le=100)] = Field(
        default_factory=list,
        description="Meal consumption percentages between 0 and 100.",
    )
    labs: dict[str, confloat(gt=0)] = Field(
        default_factory=dict,
        description="Laboratory values keyed by test name. Values must be greater than 0.",
    )
    vitals: dict[str, float | bool] = Field(
        default_factory=dict,
        description="Vital signs keyed by name; numeric values must be positive.",
    )
    problems: list[str] = Field(
        default_factory=list, description="List of patient problems."
    )
    ICD10: list[str] = Field(
        default_factory=list, description="List of ICD-10 diagnosis codes."
    )

@app.post(
    "/generate-note",
    summary="Generate clinical note",
    description=(
        "Generate a clinical note from structured patient data including glucose readings,"
        " medications, labs, vitals, and more."
    ),
)
async def generate_note(data: PatientData):
    """Create a clinical note using the provided patient data."""
    input_data = data.model_dump()
    return hoop_engine(input_data)
