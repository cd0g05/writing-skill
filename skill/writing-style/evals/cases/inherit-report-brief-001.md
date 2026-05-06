---
case_id: "inherit-report-brief-001"
category: "inheritance"
profile_fixture: "profiles/report-brief.md"
prompt_fixture: "prompts/inherit-report-brief-001.md"
expected_result_type: "human_rubric"
labels: ["inheritance", "report"]
private_terms_must_not_include: []
---

# Eval Case: inherit-report-brief-001

## User Prompt

Create `report-brief` from `report-concise`, optimized for executive skim.

## Expected Style Signals

Shorter sections, stronger summary-first structure, preserved factual discipline.

## Must Not Include

New facts or loss of source-profile relationship.

## Rubric

Score distinction from source and adherence to report style.

## Passing Criteria

Inheritance metadata exists and style match >= 4/5.
