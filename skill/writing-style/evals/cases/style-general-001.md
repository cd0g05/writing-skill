---
case_id: "style-general-001"
category: "style_match"
profile_fixture: "profiles/general-direct.md"
prompt_fixture: "prompts/general-feedback-001.md"
expected_result_type: "human_rubric"
labels: ["general", "calibration", "neutral_prompt"]
private_terms_must_not_include: []
---

# Eval Case: style-general-001

## User Prompt

Write a note that gives direct feedback while preserving trust.

## Expected Style Signals

Specific observation, direct recommendation, respectful tone, no excessive softening.

## Must Not Include

Invented personal context or workplace details.

## Rubric

Score style match, clarity, and whether the feedback avoids generic praise.

## Passing Criteria

Style match >= 4/5 and instruction adherence >= 4/5.
