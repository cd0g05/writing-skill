---
case_id: "invoke-experimental-001"
category: "instruction_adherence"
profile_fixture: "profiles/text-casual-experimental.md"
prompt_fixture: "prompts/invoke-experimental-001.md"
expected_result_type: "human_rubric"
labels: ["invocation", "experimental"]
private_terms_must_not_include: []
---

# Eval Case: invoke-experimental-001

## User Prompt

Use experimental profile `text-casual-experimental` to rewrite a short text.

## Expected Style Signals

Mentions experimental status briefly, then applies the profile if content is supplied.

## Must Not Include

Unsupported claims about the profile being ready.

## Rubric

Score whether the user is warned without derailing the task.

## Passing Criteria

Instruction adherence >= 4/5 and readiness state is accurately represented.
