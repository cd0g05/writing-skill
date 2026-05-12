# Eval Spec: Writing Skill

This local copy adapts the active Cicadas eval spec for the portable Writing Style skill. It is meant to travel with the skill and guide human or harness-based evaluation; Cicadas itself does not run evals.

## Problem and Success

Writing Style depends on LLM judgment to extract voice, generate neutral calibration samples, apply feedback, and save reusable profile instructions. Evals should catch three common failures:

- Generic "AI-polished" prose that does not match the target profile.
- Private facts, names, internal terms, or source-specific claims leaking from examples into profiles or outputs.
- Confusing how to write with what to write during saved-profile invocation.

Success means representative cases achieve:

- Style match score >= 4/5 on at least 90% of profile-creation and calibration cases.
- Privacy leakage count = 0 for default-mode saved profiles and outputs.
- 100% saved-profile schema validity.
- Instruction adherence score >= 4/5 on at least 90% of invocation cases.

## Dataset

Shared reusable cases live in `skill/writing-style/evals/cases/` and are indexed by `manifest.json`. Use synthetic or sanitized examples only. Real examples may be used in private local runs but should not be committed unless explicitly sanitized and approved.

The initial set includes 20 cases:

- 5 style-match cases across email, text, report, narrative, and general categories.
- 5 privacy-leakage cases with explicit `private_terms_must_not_include` labels.
- 4 invocation cases checking style/content separation and missing-content prompting.
- 3 profile-persistence cases checking saved profile shape and readiness behavior.
- 3 inheritance cases, including `email-professional` to `email-neutral`.

## Methodology

Run cases after material changes to `SKILL.md`, profile templates, neutral prompts, feedback rubric, privacy instructions, or validation helpers. Human review is required for subjective style match and privacy-sensitive cases. Deterministic checks may validate profile schema, required headings, status values, and absence of labeled private terms.

## Rubric

Use `../prompts/feedback-rubric.md` as the canonical rubric. Each case includes user prompt, expected style signals, must-not-include terms, rubric notes, and passing criteria.

## Exit Criteria

Before initiative completion, review the manifest and cases against the PRD, UX, and Tech Design. Blocking findings must be reflected into active specs and implementation before final validation.
