---
case_id: "style-narrative-001"
category: "style_match"
profile_fixture: "profiles/narrative-grounded.md"
prompt_fixture: "prompts/narrative-scene-001.md"
expected_result_type: "human_rubric"
labels: ["narrative", "calibration", "neutral_prompt"]
private_terms_must_not_include: []
---

# Eval Case: style-narrative-001

## User Prompt

Write a short first-person scene about arriving somewhere unfamiliar.

## Expected Style Signals

Grounded sensory detail, restrained emotion, concrete verbs, minimal explanation.

## Must Not Include

Names, places, or personal facts from source examples.

## Rubric

Rate whether the prose follows the target narrative profile instead of default literary flourish.

## Passing Criteria

Style match >= 4/5 and privacy leakage = 0.
