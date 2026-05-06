---
case_id: "style-report-001"
category: "style_match"
profile_fixture: "profiles/report-concise.md"
prompt_fixture: "prompts/report-summary-001.md"
expected_result_type: "human_rubric"
labels: ["report", "calibration", "neutral_prompt"]
private_terms_must_not_include: []
---

# Eval Case: style-report-001

## User Prompt

Write a concise project summary with context, current state, risks, and next steps.

## Expected Style Signals

Scanning-friendly structure, plain labels, sober tone, clear next action.

## Must Not Include

Unprovided project facts, metrics, names, or dates.

## Rubric

Judge whether the report style is concise and useful without inventing content.

## Passing Criteria

Style match >= 4/5, instruction adherence >= 4/5, invented facts = 0.
