function hoopEngine(data) {
  const assessmentPlan = [];
  if (data.problems && data.problems.length) {
    assessmentPlan.push(`Patient presents with: ${data.problems.join(', ')}.`);
  }
  if (data.labs && Object.keys(data.labs).length) {
    const labsSummary = Object.entries(data.labs)
      .map(([k, v]) => `${k}: ${v}`)
      .join(', ');
    assessmentPlan.push(`Recent labs: ${labsSummary}.`);
  }
  if (data.vitals && Object.keys(data.vitals).length) {
    const vitalsSummary = Object.entries(data.vitals)
      .map(([k, v]) => `${k}: ${v}`)
      .join(', ');
    assessmentPlan.push(`Vitals: ${vitalsSummary}.`);
  }
  if (data.active_meds && data.active_meds.length) {
    assessmentPlan.push(`Current medications: ${data.active_meds.join(', ')}.`);
  }
  if (data.POC_glucose && data.POC_glucose.length) {
    const glucoseValues = data.POC_glucose.join(', ');
    assessmentPlan.push(`POC Glucose readings: ${glucoseValues} mg/dL.`);
  }
  assessmentPlan.push(
    'Plan: Continue current management, encourage healthy diet and exercise, follow up in 3 months.'
  );
  return { ...data, assessment_plan: assessmentPlan };
}

module.exports = { hoopEngine };
