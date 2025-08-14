def hoop_engine(data):
    """
    Takes patient data and returns an assessment & plan.
    """

    assessment_plan = []

    # Add problems
    if data.get("problems"):
        assessment_plan.append(f"Patient presents with: {', '.join(data['problems'])}.")

    # Add labs
    if data.get("labs"):
        labs_summary = ", ".join(f"{k}: {v}" for k, v in data["labs"].items())
        assessment_plan.append(f"Recent labs: {labs_summary}.")

    # Add vitals
    if data.get("vitals"):
        vitals_summary = ", ".join(f"{k}: {v}" for k, v in data["vitals"].items())
        assessment_plan.append(f"Vitals: {vitals_summary}.")

    # Add meds
    if data.get("active_meds"):
        assessment_plan.append(f"Current medications: {', '.join(data['active_meds'])}.")

    # Add POC glucose
    if data.get("POC_glucose"):
        glucose_values = ", ".join(str(g) for g in data["POC_glucose"])
        assessment_plan.append(f"POC Glucose readings: {glucose_values} mg/dL.")

    # Add meal intake percentage
    if data.get("meal_percent"):
        avg_intake = sum(data["meal_percent"]) / len(data["meal_percent"])
        assessment_plan.append(
            f"Average meal intake: {avg_intake:.1f}%."
        )

    # Generic plan
    assessment_plan.append("Plan: Continue current management, encourage healthy diet and exercise, follow up in 3 months.")

    return {
        **data,
        "assessment_plan": assessment_plan
    }

