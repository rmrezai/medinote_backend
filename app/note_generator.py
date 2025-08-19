"""Utilities for generating assessment and plan text.

This module supports multiple strategies for crafting assessment and plan
notes. Strategy is selected via the ``NOTE_STRATEGY`` environment variable
(default: ``"rule"``). Additional configuration such as API keys or model
choices are also read from environment variables.

Currently supported strategies:

* ``rule`` - basic rule-based generator (default)
* ``llm`` - uses OpenAI's API via the ``openai`` package
"""

from __future__ import annotations

import os
from typing import Dict, List


def generate_assessment_plan(data: Dict) -> List[str]:
    """Generate an assessment & plan based on ``data``.

    Parameters
    ----------
    data:
        Patient data dictionary containing problems, labs, vitals, etc.

    Returns
    -------
    list[str]
        A list of assessment and plan strings.
    """

    strategy = os.getenv("NOTE_STRATEGY", "rule").lower()
    if strategy == "llm":
        return _generate_llm_plan(data)
    return _generate_rule_based_plan(data)


def _generate_rule_based_plan(data: Dict) -> List[str]:
    """Simple rule-based generator mirroring original behaviour."""
    assessment_plan: List[str] = []

    if data.get("problems"):
        assessment_plan.append(
            f"Patient presents with: {', '.join(data['problems'])}."
        )

    if data.get("labs"):
        labs_summary = ", ".join(f"{k}: {v}" for k, v in data["labs"].items())
        assessment_plan.append(f"Recent labs: {labs_summary}.")

    if data.get("vitals"):
        vitals_summary = ", ".join(
            f"{k}: {v}" for k, v in data["vitals"].items()
        )
        assessment_plan.append(f"Vitals: {vitals_summary}.")

    if data.get("active_meds"):
        assessment_plan.append(
            f"Current medications: {', '.join(data['active_meds'])}."
        )

    if data.get("POC_glucose"):
        glucose_values = ", ".join(str(g) for g in data["POC_glucose"])
        assessment_plan.append(
            f"POC Glucose readings: {glucose_values} mg/dL."
        )

    assessment_plan.append(
        "Plan: Continue current management, encourage healthy diet and "
        "exercise, follow up in 3 months."
    )

    return assessment_plan


def _generate_llm_plan(data: Dict) -> List[str]:
    """Generate plan text using an LLM via the OpenAI API.

    The API key is read from ``NOTE_LLM_API_KEY`` or ``OPENAI_API_KEY``.
    The model defaults to ``gpt-3.5-turbo`` but can be overridden via the
    ``NOTE_LLM_MODEL`` environment variable.
    """

    api_key = os.getenv("NOTE_LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "LLM strategy selected but no API key provided in NOTE_LLM_API_KEY "
            "or OPENAI_API_KEY"
        )

    model = os.getenv("NOTE_LLM_MODEL", "gpt-3.5-turbo")

    try:
        import openai  # type: ignore
    except Exception as exc:  # pragma: no cover - import error tested implicitly
        raise RuntimeError("openai package is required for LLM strategy") from exc

    openai.api_key = api_key
    prompt = (
        "Generate a concise medical assessment and plan based on the following "
        f"patient data: {data}"
    )
    response = openai.ChatCompletion.create(
        model=model, messages=[{"role": "user", "content": prompt}]
    )
    text = response["choices"][0]["message"]["content"].strip()
    return [text]


__all__ = ["generate_assessment_plan"]
