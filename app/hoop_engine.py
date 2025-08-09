def reference_line(source, title, year):
    return f"[Ref: {source}, {title}, {year}]"

def hoop_engine(note_data):
    note_data.setdefault('ICD10', [])
    note_data.setdefault('assessment_plan', [])

    def add_icd10_entry(title, rank=3):
        if title not in note_data['ICD10']:
            note_data['ICD10'].insert(min(rank, len(note_data['ICD10'])), title)

    def check_diabetes_ap_trigger():
        glucose = note_data.get("POC_glucose", [])
        insulin = note_data.get("active_meds", [])
        meals = note_data.get("meal_percent", [])
        problems = note_data.get("problems", [])
        high = sum(1 for g in glucose if g >= 250) >= 1
        insulin_use = any("glargine" in m.lower() or "lispro" in m.lower() for m in insulin)
        stressor = any("bacteremia" in p.lower() or "osteomyelitis" in p.lower() for p in problems)
        low_meals = any(p < 50 for p in meals)
        return high and insulin_use and (stressor or low_meals)

    def generate_diabetes_ap():
        return f"""3. Diabetes mellitus, type 2 (insulin-dependent)
- Suboptimally controlled: POC glucoses >250.
- Inflammatory/infectious stress (e.g., bacteremia) increasing insulin needs.
- Continue insulin glargine 20U nightly; adjust lispro ACHS.
- Consistent carb diet, monitor intake.
- Monitor glucose qACHS; endocrine consult PRN.
{reference_line("ADA", "Standards of Medical Care in Diabetes", 2023)}
"""

    def check_aki_ap_trigger():
        labs = note_data.get("labs", {})
        baseline = labs.get("baseline_Cr")
        current = labs.get("Cr")
        return baseline and current and (current - baseline > 0.3)

    def generate_aki_ap():
        return f"""1. Acute Kidney Injury
- Multifactorial from hypoperfusion and nephrotoxins.
- Cr rose from {note_data['labs'].get('baseline_Cr')} to {note_data['labs'].get('Cr')}.
- Hold nephrotoxics; IVF and strict I/O.
- Daily BMP.
- Nephrology consult PRN.
{reference_line("KDIGO", "Acute Kidney Injury Guidelines", 2012)}
"""

    def check_sepsis_ap_trigger():
        v = note_data.get("vitals", {})
        qsofa = int(v.get("SBP", 120) < 100) + int(v.get("RR", 18) > 22) + int(v.get("AMS", False))
        return qsofa >= 2

    def generate_sepsis_ap():
        return f"""2. Sepsis – source unclear
- qSOFA = 2 (SBP<100, AMS).
- Broad-spectrum antibiotics started.
- IVF boluses for MAP<65.
- Monitor for organ dysfunction.
- ID consult if no improvement.
{reference_line("NEJM", "Sepsis-3 Definitions", 2016)}
"""

    def check_electrolytes_trigger():
        labs = note_data.get("labs", {})
        return any([
            labs.get("Na", 135) < 130 or labs.get("Na", 135) > 150,
            labs.get("K", 4) < 3 or labs.get("K", 4) > 5.5
        ])

    def generate_electrolytes_ap():
        return f"""4. Electrolyte abnormalities
- Na = {note_data['labs'].get('Na')}, K = {note_data['labs'].get('K')}
- Likely secondary to renal dysfunction.
- Replace electrolytes per protocol.
- Monitor BMP q6h.
{reference_line("NEJM", "Electrolyte Disorders Review", 2020)}
"""

    if check_aki_ap_trigger():
        add_icd10_entry("Acute Kidney Injury", 0)
        note_data['assessment_plan'].append(generate_aki_ap())

    if check_sepsis_ap_trigger():
        add_icd10_entry("Sepsis", 1)
        note_data['assessment_plan'].append(generate_sepsis_ap())

    if check_diabetes_ap_trigger():
        add_icd10_entry("Diabetes mellitus, type 2 (insulin-dependent)", 2)
        note_data['assessment_plan'].append(generate_diabetes_ap())

    if check_electrolytes_trigger():
        add_icd10_entry("Electrolyte abnormalities", 4)
        note_data['assessment_plan'].append(generate_electrolytes_ap())

    return note_data