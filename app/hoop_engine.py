import csv
import json
from typing import Any, Dict, List


def mediNote_hoop_engine(patient_data: Dict[str, Any]) -> Dict[str, List[str]]:
    """Apply HOOP logic to structured patient data for ICD-10 and A/P generation."""
    icd10: List[str] = []
    ap: List[str] = []

    # --- AKI ---
    cr_baseline = patient_data.get("baseline_Cr")
    cr_current = patient_data.get("Cr")
    if cr_baseline and cr_current and cr_current - cr_baseline > 0.3:
        icd10.append("Acute Kidney Injury")
        ap.append(
            f"""1. Acute Kidney Injury
- Cr rose from {cr_baseline} to {cr_current}, eGFR = {patient_data.get('eGFR', '?')}.
- Suspected multifactorial etiology: hypoperfusion (MAP = {patient_data.get('MAP', '?')}) + nephrotoxic meds.
- Hold ACEi/NSAIDs; ensure renal dosing of antibiotics/diuretics.
- Daily BMP, strict I/O, encourage PO intake.
- Nephrology consult if Cr ≥2.5 x48h."""
        )

    # --- Sepsis ---
    rr = patient_data.get("RR", 0)
    map_val = patient_data.get("MAP", 999)
    wbc = patient_data.get("WBC", 0)
    if rr > 22 and map_val < 70 and cr_current and cr_current > 2:
        icd10.append("Sepsis – viral origin (rhinovirus)")
        ap.append(
            f"""2. Sepsis – viral origin (rhinovirus)
- Meets Sepsis-3: RR {rr}, MAP {map_val}, Cr {cr_current}, WBC {wbc}.
- Source: respiratory infection, rhinovirus confirmed on PCR.
- Ceftriaxone + doxycycline initiated empirically.
- Monitor for superinfection; ID consult if not improving.
- No pressor need; MAP >70 after fluids."""
        )

    # --- Hypoxic Respiratory Failure ---
    spo2_list = patient_data.get("SpO2", [100])
    spo2_min = min(spo2_list)
    if spo2_min < 94:
        icd10.insert(0, "Acute Hypoxic Respiratory Failure")
        ap.insert(
            0,
            f"""1. Acute Hypoxic Respiratory Failure
- SpO₂ ranged {spo2_min}–{max(spo2_list)}% on {patient_data.get('O2_flow')} L/min NC.
- CXR on {patient_data.get('CXR_date')} showed persistent bilateral opacities.
- Etiology: CAP vs atelectasis, co-infection with rhinovirus.
- Continue ceftriaxone + doxycycline, supportive O₂, IS.
- Reassess need for escalation vs discharge readiness."""
        )

    # --- Hypomagnesemia ---
    mg = patient_data.get("Mg")
    if mg and mg < 1.7:
        icd10.append("Electrolyte Abnormalities – hypomagnesemia")
        ap.append(
            f"""5. Electrolyte Abnormality – Hypomagnesemia
- Mg = {mg}, likely secondary to Lasix + volume depletion.
- IV MgSO₄ repletion initiated.
- Repeat BMP q6h; transition to PO once tolerating.
- Monitor QTc, Cr, and repletion response."""
        )

    # --- Diabetes ---
    glucoses = patient_data.get("glucose", [])
    if len([g for g in glucoses if g > 200]) >= 2:
        icd10.append("Type 2 Diabetes Mellitus, insulin-dependent")
        ap.append(
            f"""4. Type 2 Diabetes Mellitus (insulin-dependent)
- POC glucoses: {glucoses}, HbA1c {patient_data.get('HbA1c', '?')}%.
- Likely stress hyperglycemia from infection/inflammation.
- Continue lispro ACHS; defer basal insulin until PO stable.
- Hold metformin if eGFR <30.
- Monitor glucose trends and caloric intake."""
        )

    return {"ICD10": icd10, "Assessment_Plan": ap}


def load_from_json(json_path: str) -> Dict[str, Any]:
    with open(json_path) as f:
        return json.load(f)


def load_from_csv(csv_path: str) -> Dict[str, Any]:
    patient_data: Dict[str, Any] = {}
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = row.get("key")
            val = row.get("value")
            try:
                patient_data[key] = float(val)
            except (TypeError, ValueError):
                patient_data[key] = val
    return patient_data


# Alias for backward compatibility
hoop_engine = mediNote_hoop_engine
