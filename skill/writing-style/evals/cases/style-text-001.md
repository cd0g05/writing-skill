---
case_id: "style-text-001"
category: "style_match"
profile_fixture: "profiles/text-casual.md"
prompt_fixture: "prompts/text-late-001.md"
expected_result_type: "human_rubric"
labels: ["text", "calibration", "neutral_prompt"]
private_terms_must_not_include: []
---

# Eval Case: style-text-001

## User Prompt

Write a short text saying you are running ten minutes late and will follow up soon.

## Expected Style Signals

Concise, natural, lightly apologetic, no overexplaining, no stiff punctuation.

## Must Not Include

Private location, event, or recipient details.

## Rubric

Score style match and whether the message feels like a plausible short text rather than an email.

## Passing Criteria

Style match >= 4/5 and no invented facts.
