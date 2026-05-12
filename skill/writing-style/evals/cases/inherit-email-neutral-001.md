---
case_id: "inherit-email-neutral-001"
category: "inheritance"
profile_fixture: "profiles/email-neutral.md"
prompt_fixture: "prompts/inherit-email-neutral-001.md"
expected_result_type: "human_rubric"
labels: ["inheritance", "email"]
private_terms_must_not_include: []
---

# Eval Case: inherit-email-neutral-001

## User Prompt

Create `email-neutral` from `email-professional`, making it less formal and shorter.

## Expected Style Signals

Keeps clear asks and warmth while reducing formality and length.

## Must Not Include

Mutation of the source profile.

## Rubric

Review the style diff for Keep, Change, and Avoid decisions.

## Passing Criteria

New profile has `source_profile`, meaningful distinction, and source remains unchanged.
