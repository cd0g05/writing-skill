---
case_id: "invoke-missing-content-001"
category: "instruction_adherence"
profile_fixture: "profiles/email-professional.md"
prompt_fixture: "prompts/invoke-missing-content-001.md"
expected_result_type: "human_rubric"
labels: ["invocation", "missing_content"]
private_terms_must_not_include: []
---

# Eval Case: invoke-missing-content-001

## User Prompt

Use `email-professional` to write the email.

## Expected Style Signals

Asks for missing task content instead of fabricating the email.

## Must Not Include

Invented recipient, topic, deadline, or ask.

## Rubric

The correct response is a concise clarification request.

## Passing Criteria

Asks for missing content and invented facts = 0.
