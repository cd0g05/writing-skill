---
case_id: "persist-ready-001"
category: "profile_persistence"
profile_fixture: "profiles/email-professional.md"
prompt_fixture: "prompts/persist-ready-001.md"
expected_result_type: "deterministic_check"
labels: ["persistence", "ready"]
private_terms_must_not_include: []
---

# Eval Case: persist-ready-001

## User Prompt

Save a profile after two consecutive approved calibration outputs.

## Expected Style Signals

Profile front matter marks `status: "ready"` and `consecutive_passes: 2`.

## Must Not Include

Missing required headings or vague readiness notes.

## Rubric

Run profile validation and inspect readiness fields.

## Passing Criteria

Validation passes and readiness criteria are visible.
