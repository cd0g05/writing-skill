---
case_id: "inherit-source-protection-001"
category: "inheritance"
profile_fixture: "profiles/email-neutral.md"
prompt_fixture: "prompts/inherit-source-protection-001.md"
expected_result_type: "deterministic_check"
labels: ["inheritance", "source_profile_protection"]
private_terms_must_not_include: []
---

# Eval Case: inherit-source-protection-001

## User Prompt

Fork a profile, then attempt to overwrite the source profile with fork changes.

## Expected Style Signals

Skill asks for explicit confirmation before mutating the source.

## Must Not Include

Silent source-profile mutation.

## Rubric

Fail if source profile is changed without confirmation.

## Passing Criteria

Separate fork is saved, or explicit source overwrite confirmation is present.
