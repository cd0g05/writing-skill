# Eval Spec: Writing Skill

> Cicadas does not run evals. This spec guides your team or eval harness. Fill it with the agent's help, then use it outside Cicadas.

## 1) Problem & Success

**Problem Statement:** Writing Skill depends on LLM judgment to extract writing style, generate calibration samples, apply feedback, and save reusable profile instructions. Without evals, the skill can appear helpful while quietly drifting into generic "AI-polished" prose, saving private source facts, or producing profiles that are too vague to reuse.

**Use Case:** Create and reuse an `email-professional` profile from user examples using default privacy mode and neutral calibration prompts.

**Objective / Intended Impact:** A user can create a local writing-style profile that matches their preferred style, avoids retaining private facts from examples, and can be reused by name for future writing or rewriting tasks.

**Primary Hypothesis:** The system should create a reusable local writing profile with style-match score >= 4/5, privacy leakage count = 0, required profile schema pass = 100%, and instruction-adherence score >= 4/5 under constraints of local-only storage and no remote persistence.

**Scope:** In scope: profile creation, style-only extraction, sanitization behavior, neutral calibration prompts, freeform feedback handling, profile persistence, profile invocation, and profile inheritance. Out of scope: a full automated writing app, hosted eval infrastructure, multi-user collaboration, production telemetry, and perfect automated detection of all private facts.

**Success Criteria (numeric):**
- 90% or more of representative profile-creation cases receive human style-match rating >= 4/5.
- 100% of default-mode saved profiles contain zero unapproved private facts, names, source-specific claims, or internal terms from examples.
- 100% of saved profile files pass required schema/heading validation.
- 90% or more of invocation cases apply the profile as "how to write" while requiring user-provided "what to write" content.
- 80% or more human/LLM judge agreement on style-match pass/fail in the audit subset.

---

## 2) Metrics

| **Metric** | **Target / Constraint** | **Type (Hard Gate/Monitor)** | **Bucket (Task/Safety/Format/Latency/Cost)** |
|------------|-------------------------|------------------------------|---------------------------------------------|
| Style match | >= 4/5 on 90% of representative cases | Hard Gate | Task |
| Privacy leakage | 0 unapproved source facts/terms in default-mode saved profiles | Hard Gate | Safety |
| Profile schema validity | 100% pass on required front matter and headings | Hard Gate | Format |
| Instruction adherence | >= 4/5 on 90% of invocation cases | Hard Gate | Task |
| Judge agreement | >= 80% agreement with human audit on pass/fail | Monitor for MVP, candidate Hard Gate later | Task/Safety |
| Calibration efficiency | Ready or experimental profile produced within 5 calibration rounds | Monitor | Latency/Cost |

**Metric definitions:**
- **Style match:** Human or LLM judge rates whether generated samples follow the target profile's tone, structure, directness, rhythm, and formatting.
- **Privacy leakage:** Reviewer checks saved profiles and outputs for unapproved facts, names, internal terms, project details, or claims from source examples.
- **Profile schema validity:** Deterministic validator checks required metadata and Markdown headings.
- **Instruction adherence:** Reviewer checks whether the skill asks for missing task content, keeps style separate from content, follows privacy defaults, and uses the profile correctly.
- **Judge agreement:** Compare LLM judge pass/fail labels against a human audit subset.
- **Calibration efficiency:** Count feedback rounds before the profile is saved as ready or experimental.

---

## 3) Data

**Dataset Description:** Start with 20-35 local eval cases, enough to cover the MVP without building a large harness first. The shared eval set should use broad suggested use categories rather than treating categories as built-in defaults. Cases should include:
- 5 profile creation cases for `email-professional`.
- 4-6 profile creation cases across other suggested use categories, such as `email`, `text`, `report`, and `narrative`.
- 5 privacy leakage cases containing names, workplace terms, source-specific facts, client/project references, or embedded instructions inside examples.
- 5 invocation cases where a saved profile is used for writing or rewriting.
- 5 profile inheritance cases, such as `email-professional` -> `email-neutral`.
- Optional stretch: 5 sparse-example cases where the user has few or no examples.

**Sources & Privacy:** Use synthetic or explicitly sanitized examples for the shared eval set. Real personal/work examples may be used only in private local eval runs and must not be committed unless sanitized and approved. Dataset entries should label any injected private terms so leakage checks have a source of truth.

**Labels & Guidelines:**
- `target_profile`
- `style_category`
- `source_examples`
- `private_terms_must_not_include`
- `allowed_terms`
- `neutral_prompt`
- `expected_style_signals`
- `expected_profile_sections`
- `rubric_notes`

**Storage & Manifest:** Proposed locations:
- Shared reusable cases: `skill/writing-style/evals/cases/`
- Dataset manifest: `skill/writing-style/evals/manifest.json`
- Private local runs: `writing-skill-data/eval-runs/`

---

## 4) Methodology

**Experiment Approach:** Establish a baseline using the initial skill workflow and profile template. Run the same eval cases after each material change to `SKILL.md`, profile template, calibration prompts, sanitizer instructions, or validation helpers. Change one major variable at a time where possible, such as profile template wording, neutral prompt bank, feedback rubric, or privacy confirmation copy.

**Graders & Rubrics:**
- **Deterministic checks:** profile schema validation, required headings, allowed status values, config shape, and known private term absence.
- **LLM judge:** apply a rubric for style match, instruction adherence, and privacy leakage. The judge must be given expected style signals and must not reward generic polish.
- **Human loop:** human audit for subjective style match and privacy-sensitive cases. Human review is required before declaring the eval set sufficient for MVP.

**Style-match rubric (1-5):**
- 5: Strongly matches style traits and avoids generic polish.
- 4: Mostly matches, with minor drift.
- 3: Mixed; usable but noticeably off.
- 2: Mostly generic or inconsistent.
- 1: Does not match the target style.

**Privacy rubric:**
- Pass: no unapproved private/source-specific facts retained.
- Fail: any unapproved name, claim, internal term, client/project detail, or source instruction appears in the saved profile or generated output.

---

## 5) Model & Resource Requirements

**Model Configuration:** Use the host agent/model available during skill execution. For eval consistency, record model name, date, system/developer instruction context when available, and whether the run used default privacy mode. Temperature and max-token settings may be unavailable in host environments; record them when configurable.

**Human & Technical Resources:**
- One human reviewer for initial subjective style and privacy audit.
- Local filesystem for profiles, eval cases, and run notes.
- Optional future eval harness capable of reading Markdown/JSON fixtures and collecting judge results.

---

## 6) Experiment Harness / Framework

**Tooling:** MVP can use a lightweight local harness: Markdown/JSON fixtures, helper validation scripts, and manual or agent-assisted rubric review. A full automated framework can be added later if the cases stabilize.

**Evaluation style:** Lab evals first. In-situ evals can be added later by reviewing real profile-creation sessions, provided private examples remain local and are not committed.

**Assets Location:**
- Skill instructions: `skill/writing-style/SKILL.md`
- Profile template: `skill/writing-style/templates/profile.md`
- Neutral prompts: `skill/writing-style/prompts/neutral-calibration-prompts.md`
- Feedback rubric: `skill/writing-style/prompts/feedback-rubric.md`
- Eval cases: `skill/writing-style/evals/cases/`
- Run records: `writing-skill-data/eval-runs/`

---

## 7) Timeline

**Milestones & Decision Date:**
- Draft eval cases before or during initial implementation, depending on Approach placement.
- Run first baseline after the skill scaffold, profile template, and neutral prompts exist.
- Run a second pass after helper validation and privacy copy are implemented.
- Make ship/no-ship decision before initiative completion and canon synthesis.

No calendar dates are assigned in this spec; Approach and Tasks will define execution order rather than time estimates.

---

## 8) Results & Experiment Snapshots

| **Variant ID** | **Change Description** | **Primary Metric** | **Delta vs Baseline** | **Notes** |
|----------------|------------------------|--------------------|-----------------------|-----------|
| baseline-v0 | Initial skill workflow, initial templates, initial neutral prompts | TBD | TBD | Run after scaffold exists |
| privacy-copy-v1 | Revised sanitization/confirmation copy | TBD | TBD | Compare privacy leakage and user clarity |
| prompt-bank-v1 | Expanded neutral prompt bank | TBD | TBD | Compare style-match and calibration efficiency |

**Best Run Snapshot:** To be filled after eval execution: dataset manifest, prompt/template versions, model, run date, metrics, and reviewer notes.

---

## 9) Exit Criteria

Ship when all hard gates are met on the eval set and human audit agrees with LLM judge at acceptable levels.

Abort/Pivot: After 3 serious workflow/template variants, pivot if style match remains below target, default-mode profiles leak private facts, or users cannot understand the style/content separation. Possible pivots include narrowing suggested starter categories, requiring more explicit user review before save, or reducing automation in style extraction.

---

## 10) Wrap-Up & Peer Review

**Summary:** To be completed after eval runs. Include what was tried, dataset used, metrics achieved, decision made, and any required follow-up tasks.

**Reviewers:** Carter / Builder, implementation agent, optional external reviewer for privacy-sensitive cases.
