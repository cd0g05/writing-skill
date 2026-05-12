---
case_id: "invoke-rewrite-001"
category: "instruction_adherence"
profile_fixture: "profiles/report-concise.md"
prompt_fixture: "prompts/invoke-rewrite-001.md"
expected_result_type: "human_rubric"
labels: ["invocation", "rewrite"]
private_terms_must_not_include: []
---

# Eval Case: invoke-rewrite-001

## User Prompt

Rewrite a dense status paragraph using `report-concise` without changing the facts.

## Expected Style Signals

Clearer structure, shorter sentences, same factual content.

## Must Not Include

New claims, metrics, owners, or dates.

## Rubric

Fail if rewrite changes factual meaning or invents missing details.

## Passing Criteria

Instruction adherence >= 4/5 and factual drift = 0.
