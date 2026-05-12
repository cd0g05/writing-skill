---
case_id: "invoke-write-001"
category: "instruction_adherence"
profile_fixture: "profiles/email-professional.md"
prompt_fixture: "prompts/invoke-write-001.md"
expected_result_type: "human_rubric"
labels: ["invocation", "write"]
private_terms_must_not_include: []
---

# Eval Case: invoke-write-001

## User Prompt

Use `email-professional` to write a follow-up using these facts: the draft is ready, review is requested by Friday, and comments can be inline.

## Expected Style Signals

Applies profile style while using only supplied facts.

## Must Not Include

Unprovided reasons, deadlines, names, or project context.

## Rubric

Score whether profile controls style and prompt controls content.

## Passing Criteria

Instruction adherence >= 4/5 and invented facts = 0.
