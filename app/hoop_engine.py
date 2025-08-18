"""Utilities for generating a patient assessment and plan."""

from typing import Any, Callable, Dict, Iterable, List, Optional


def format_problems(problems: Iterable[str]) -> str:
    """Return a sentence summarizing the patient's problems."""

    return f"Patient presents with: {', '.join(problems)}."


def format_labs(labs: Dict[str, Any]) -> str:
    """Return a sentence summarizing recent laboratory values."""

    summary = ", ".join(f"{k}: {v}" for k, v in labs.items())
    return f"Recent labs: {summary}."


def format_vitals(vitals: Dict[str, Any]) -> str:
    """Return a sentence summarizing current vital signs."""

    summary = ", ".join(f"{k}: {v}" for k, v in vitals.items())
    return f"Vitals: {summary}."


def format_meds(meds: Iterable[str]) -> str:
    """Return a sentence summarizing active medications."""

    return f"Current medications: {', '.join(meds)}."


def format_poc_glucose(readings: Iterable[Any]) -> str:
    """Return a sentence summarizing point-of-care glucose readings."""

    values = ", ".join(str(g) for g in readings)
    return f"POC Glucose readings: {values} mg/dL."


DEFAULT_PLAN = [
    "Plan: Continue current management, encourage healthy diet and exercise, follow up in 3 months."
]


def hoop_engine(
    data: Dict[str, Any],
    include_sections: Optional[Iterable[str]] = None,
    plan: Optional[Iterable[str]] = None,
) -> Dict[str, Any]:
    """Generate an assessment and plan from patient data.

    Parameters
    ----------
    data:
        Patient data dictionary. Keys correspond to available sections such as
        ``problems``, ``labs``, ``vitals``, ``active_meds`` and ``POC_glucose``.
    include_sections:
        Iterable of section names to include. If ``None`` (default), all
        available sections present in ``data`` are used.
    plan:
        Iterable of plan strings to append to the assessment. If ``None``
        (default), a generic plan is used.

    Returns
    -------
    dict
        The input ``data`` with an added ``assessment_plan`` list.
    """

    assessment_plan: List[str] = []

    section_formatters: Dict[str, Callable[[Any], str]] = {
        "problems": format_problems,
        "labs": format_labs,
        "vitals": format_vitals,
        "active_meds": format_meds,
        "POC_glucose": format_poc_glucose,
    }

    sections_to_include = (
        set(include_sections) if include_sections is not None else section_formatters.keys()
    )

    for section, formatter in section_formatters.items():
        if section in sections_to_include and data.get(section):
            assessment_plan.append(formatter(data[section]))

    plan_items = list(plan) if plan is not None else DEFAULT_PLAN
    assessment_plan.extend(plan_items)

    return {**data, "assessment_plan": assessment_plan}

