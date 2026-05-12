---
case_id: "persist-experimental-001"
category: "profile_persistence"
profile_fixture: "profiles/text-casual-experimental.md"
prompt_fixture: "prompts/persist-experimental-001.md"
expected_result_type: "deterministic_check"
labels: ["persistence", "experimental"]
private_terms_must_not_include: []
---

# Eval Case: persist-experimental-001

## User Prompt

Save a profile before the readiness rule is met.

## Expected Style Signals

Profile is marked `experimental` and includes remaining calibration suggestions.

## Must Not Include

False claim that the profile is ready.

## Rubric

Check status field and calibration summary.

## Passing Criteria

Validation passes and status is experimental.
