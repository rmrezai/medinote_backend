const test = require('node:test');
const assert = require('node:assert/strict');
const { hoopEngine } = require('./hoopEngine');

test('builds assessment plan from data', () => {
  const data = {
    problems: ['Hypertension'],
    labs: { A1C: '7%' },
    vitals: { BP: '120/80' },
    active_meds: ['Metformin'],
    POC_glucose: [110, 115],
  };
  const result = hoopEngine(data);
  assert.ok(result.assessment_plan.includes('Patient presents with: Hypertension.'));
  assert.ok(result.assessment_plan.includes('Recent labs: A1C: 7%.'));
  assert.ok(result.assessment_plan.includes('Vitals: BP: 120/80.'));
  assert.ok(result.assessment_plan.includes('Current medications: Metformin.'));
  assert.ok(result.assessment_plan.includes('POC Glucose readings: 110, 115 mg/dL.'));
  assert.ok(result.assessment_plan.includes('Plan: Continue current management, encourage healthy diet and exercise, follow up in 3 months.'));
});
