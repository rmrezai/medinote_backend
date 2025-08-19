"""Core engine for generating patient notes."""

from .note_generator import generate_assessment_plan


def hoop_engine(data):
    """Create a response containing an assessment & plan.

    Parameters
    ----------
    data:
        Patient information to be fed to the note generator.

    Returns
    -------
    dict
        Original data augmented with ``assessment_plan`` key.
    """

    assessment_plan = generate_assessment_plan(data)

    return {**data, "assessment_plan": assessment_plan}

