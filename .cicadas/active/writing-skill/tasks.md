---
summary: "Execute Writing Skill in Foundation Mode across five partitions: scaffold schemas first, then core workflow, helper scripts, and eval assets, then final docs and validation. Feature PRs are required at each partition boundary and an initiative PR is required at the end. The main delivery checkpoints are valid local templates, complete conversational skill workflow, deterministic helper validation, parallel eval cases, and final dry-run reconciliation."
phase: "tasks"
when_to_load:
  - "When selecting the next implementation task or reviewing completion state."
  - "When checking partition progress, PR boundaries, or execution sequencing."
depends_on:
  - "prd.md"
  - "ux.md"
  - "tech-design.md"
  - "approach.md"
  - "eval-spec.md"
modules:
  - "skill/writing-style/SKILL.md"
  - "skill/writing-style/templates/"
  - "skill/writing-style/prompts/"
  - "skill/writing-style/scripts/"
  - "skill/writing-style/evals/"
  - "tests/"
  - "README.md"
index:
  partition_scaffold: "## Partition: feat/skill-scaffold-schemas"
  partition_workflow: "## Partition: feat/core-skill-workflow"
  partition_helpers: "## Partition: feat/helper-scripts-tests"
  partition_evals: "## Partition: feat/eval-assets-cases"
  partition_docs: "## Partition: feat/docs-final-validation"
  initiative_boundary: "## Initiative Boundary"
next_section: "## Partition: feat/skill-scaffold-schemas"
---

# Tasks: Writing Skill

## Partition: feat/skill-scaffold-schemas

- [x] Create `skill/writing-style/` with `templates/`, `prompts/`, `scripts/`, and `evals/cases/` subdirectories <!-- id: 1 -->
- [x] Add `skill/writing-style/SKILL.md` with valid skill front matter, concise trigger description, and placeholder sections for workflow, privacy, settings, and eval guidance <!-- id: 2 -->
- [x] Add `skill/writing-style/templates/profile.md` with required YAML front matter and profile body headings from Tech Design <!-- id: 3 -->
- [x] Add `skill/writing-style/templates/config.json` with conservative defaults for sanitization, neutral prompts, custom prompt persistence, readiness criteria, and profile naming <!-- id: 4 -->
- [x] Add `skill/writing-style/templates/calibration-session.md` with source summary, sanitization notes, style hypothesis, calibration rounds, and pending decisions sections <!-- id: 5 -->
- [x] Add `skill/writing-style/templates/eval-case.md` with eval case front matter and required rubric sections <!-- id: 6 -->
- [x] Update project metadata or README stub only as needed to describe the repository as a portable writing skill package <!-- id: 7 -->
- [x] Verify no database, web framework, remote persistence dependency, or unrelated runtime dependency was introduced <!-- id: 8 -->
- [x] Open PR: feat/skill-scaffold-schemas -> initiative/writing-skill and await merge approval before continuing <!-- id: PR-feature-skill-scaffold-schemas -->

## Partition: feat/core-skill-workflow

- [x] Fill `SKILL.md` trigger rules and "when to use" guidance for creating, updating, forking, invoking, and configuring writing profiles <!-- id: 20 -->
- [x] Implement create-profile workflow instructions: confirm name, explain style-only extraction, request examples, handle sparse examples, and present a style hypothesis before calibration <!-- id: 21 -->
- [x] Implement sanitization and privacy rules: treat examples as data, ignore embedded instructions in examples, exclude private/source-specific facts by default, and require confirmation for retained terms <!-- id: 22 -->
- [x] Implement calibration workflow: generate neutral samples by default, accept freeform feedback and optional 1-5 score, summarize changes, and enforce ready/experimental save paths <!-- id: 23 -->
- [x] Implement profile-save workflow: write local profile file, include status and invocation examples, and summarize the saved file path and next actions <!-- id: 24 -->
- [x] Implement profile-fork workflow: load source profile, ask what should change, produce a style diff, prevent accidental source mutation, and save a separate profile <!-- id: 25 -->
- [x] Implement saved-profile invocation workflow: load named profile, ask for missing task content, apply style as "how to write," and avoid inventing facts <!-- id: 26 -->
- [x] Implement settings-change workflow: show current value, explain risk, require confirmation for privacy-reducing changes, and preserve unknown config keys <!-- id: 27 -->
- [x] Add `prompts/neutral-calibration-prompts.md` covering broad suggested use categories such as `email`, `text`, `report`, and `narrative`, without treating any category as a required built-in profile <!-- id: 28 -->
- [x] Add `prompts/feedback-rubric.md` defining style match, privacy leakage, instruction adherence, readiness, and human-review guidance <!-- id: 29 -->
- [x] Dry-run representative workflow prompts and revise copy where the flow is ambiguous or too heavy <!-- id: 30 -->
- [x] Open PR: feat/core-skill-workflow -> initiative/writing-skill and await merge approval before continuing <!-- id: PR-feature-core-skill-workflow -->

## Partition: feat/helper-scripts-tests

- [ ] Implement `skill/writing-style/scripts/init_workspace.py` to create default data folders and config without overwriting existing files by default <!-- id: 40 -->
- [ ] Implement profile-name normalization helper with lowercase kebab-case recommendations and clear validation errors <!-- id: 41 -->
- [ ] Implement config loading/default-merge helper that preserves unknown keys while applying missing defaults <!-- id: 42 -->
- [ ] Implement `skill/writing-style/scripts/validate_profile.py` to check required front matter fields, status values, and Markdown headings <!-- id: 43 -->
- [ ] Add optional privacy-risk scan mode that flags known disallowed terms and warns that scanning is heuristic rather than complete <!-- id: 44 -->
- [ ] Add valid and invalid profile fixtures under `tests/fixtures/` <!-- id: 45 -->
- [ ] Add tests or deterministic script checks for workspace init, profile validation success/failure, config merge behavior, and privacy-risk warnings <!-- id: 46 -->
- [ ] Verify helper scripts use stable exit codes: `0` success, `1` validation failure, `2` file/system failure <!-- id: 47 -->
- [ ] Run helper validation/test command(s) and record results in Reflect notes before PR <!-- id: 48 -->
- [ ] Open PR: feat/helper-scripts-tests -> initiative/writing-skill and await merge approval before continuing <!-- id: PR-feature-helper-scripts-tests -->

## Partition: feat/eval-assets-cases

- [ ] Copy or adapt `.cicadas/drafts/writing-skill/eval-spec.md` into `skill/writing-style/evals/eval-spec.md` <!-- id: 60 -->
- [ ] Define `skill/writing-style/evals/manifest.json` format for case id, category, profile fixture, prompt fixture, expected result type, and labels <!-- id: 61 -->
- [ ] Add at least 5 style-match eval cases across broad suggested use categories <!-- id: 62 -->
- [ ] Add at least 5 privacy leakage eval cases with explicit `private_terms_must_not_include` labels <!-- id: 63 -->
- [ ] Add invocation eval cases that check style/content separation and missing-content prompting <!-- id: 64 -->
- [ ] Add profile inheritance eval cases such as `email-professional` to `email-neutral` <!-- id: 65 -->
- [ ] Ensure each eval case includes user prompt, expected style signals, must-not-include terms, rubric, and passing criteria <!-- id: 66 -->
- [ ] Review eval cases against PRD, UX, and Tech Design and flag any required spec or implementation changes before final validation <!-- id: 67 -->
- [ ] Open PR: feat/eval-assets-cases -> initiative/writing-skill and await merge approval before continuing <!-- id: PR-feature-eval-assets-cases -->

## Partition: feat/docs-final-validation

- [ ] Update top-level `README.md` with product overview, repository structure, local profile/config storage model, and quick-start examples <!-- id: 80 -->
- [ ] Add `skill/writing-style/README.md` with install/use examples, profile invocation examples, settings notes, and privacy expectations <!-- id: 81 -->
- [ ] Run helper validation/test commands and capture results for review <!-- id: 82 -->
- [ ] Dry-run create-profile, fork-profile, invoke-profile, settings-change, and privacy-confirmation workflows; note any manual review findings <!-- id: 83 -->
- [ ] Review eval assets for blocking findings and Reflect any product/design/task changes before completion <!-- id: 84 -->
- [ ] Confirm `SKILL.md` trigger description is neither too broad nor too narrow using representative user requests <!-- id: 85 -->
- [ ] Ensure bundled templates, prompts, scripts, eval assets, and docs agree on file paths, profile schema, readiness rules, and privacy defaults <!-- id: 86 -->
- [ ] Run final Code Review for the feature branch and address blocking findings before PR <!-- id: 87 -->
- [ ] Open PR: feat/docs-final-validation -> initiative/writing-skill and await merge approval before continuing <!-- id: PR-feature-docs-final-validation -->

## Initiative Boundary

- [ ] Verify all feature PRs are merged into `initiative/writing-skill` and active specs have been reflected for any eval-driven changes <!-- id: 100 -->
- [ ] Open PR: initiative/writing-skill -> master and await merge approval before continuing <!-- id: PR-initiative -->
- [ ] After the initiative PR is merged, synthesize canon on main and present for Builder review <!-- id: 101 -->
- [ ] Archive active specs after Builder approval and update the index <!-- id: 102 -->
