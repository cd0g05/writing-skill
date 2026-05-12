---
case_id: "style-email-001"
category: "style_match"
profile_fixture: "profiles/email-professional.md"
prompt_fixture: "prompts/email-followup-001.md"
expected_result_type: "human_rubric"
labels: ["email", "calibration", "neutral_prompt"]
private_terms_must_not_include: []
---

# Eval Case: style-email-001

## User Prompt

Create a neutral calibration email asking whether a teammate has what they need to move a task forward.

## Expected Style Signals

Direct opening, brief context, clear ask, warm but not overly polished close.

## Must Not Include

Source-specific project names, workplace names, or claims from examples.

## Rubric

Rate style match using the feedback rubric. Penalize generic corporate filler.

## Passing Criteria

Style match >= 4/5, instruction adherence >= 4/5, privacy leakage = 0.
