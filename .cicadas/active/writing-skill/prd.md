---
summary: "Writing Skill is an LLM skill for creating reusable local writing-style profiles. It guides a user through example intake, style-only analysis, neutral calibration prompts, freeform grading, and iterative refinement until the user approves a saved profile that can later be invoked by name for writing or rewriting tasks. The product defaults to privacy-preserving behavior: sanitize examples, avoid retaining factual content from samples, use neutral prompts, and require explicit confirmation before riskier settings are changed."
phase: "clarify"
when_to_load:
  - "When defining or reviewing Writing Skill goals, users, scope, success criteria, and privacy expectations."
  - "When validating that later UX, tech design, implementation, and eval work still align with the intended style-calibration product."
depends_on: []
modules:
  - "LLM skill workflow"
  - "Local style profile storage"
  - "Calibration and eval flow"
  - "Privacy and settings defaults"
index:
  executive_summary: "## Executive Summary"
  project_classification: "## Project Classification"
  success_criteria: "## Success Criteria"
  user_journeys: "## User Journeys"
  scope: "## Scope"
  functional_requirements: "## Functional Requirements"
  non_functional_requirements: "## Non-Functional Requirements"
  open_questions: "## Open Questions"
  risk_mitigation: "## Risk Mitigation"
next_section: "UX"
---

# PRD: Writing Skill

## Progress

- [x] Executive Summary
- [x] Project Classification
- [x] Success Criteria
- [x] User Journeys
- [x] Scope & Phasing
- [x] Functional Requirements
- [x] Non-Functional Requirements
- [x] Open Questions
- [x] Risk Mitigation

## Executive Summary

Writing Skill is an LLM skill that helps a user teach an LLM their preferred writing styles and save those styles as reusable local profiles. It turns user-provided examples into style-only instructions, then runs calibration cycles where the model produces neutral test samples, the user grades them, and the profile is refined until it reliably captures how the user wants a given kind of writing to sound.

The most important outcome is a durable library of user-created named writing profiles, such as `email`, `text`, `report`, or `narrative`, that describe how to write without absorbing private facts from the source examples.

### What Makes This Special

- **Style learning without fact retention** — The skill explicitly separates voice, rhythm, structure, tone, and preference from names, business details, claims, and private context embedded in examples.
- **Interactive calibration loop** — The user does not need to write perfect instructions up front; they can provide examples, react to generated samples, and let the profile improve through feedback.
- **Local reusable profiles** — Approved styles are saved as local files, making them inspectable, editable, versionable, and reusable across future writing tasks.
- **Safe defaults with explicit override** — The skill defaults to neutral prompts, sanitization, and non-retention of sample content, while still allowing intentional overrides after confirmation.
- **Profile inheritance** — New styles can start from existing styles, such as deriving `email-neutral` from `email-professional`, so the library can grow without starting from scratch each time.

## Project Classification

**Technical Type:** Agent Skill / Developer-Adjacent Productivity Tool
**Domain:** Writing, Personal Productivity, LLM Personalization
**Complexity:** Medium — The product is not a large application, but it requires careful prompt workflow design, local artifact structure, privacy defaults, user feedback handling, and eval support.
**Project Context:** Brownfield repository with Cicadas already present, but the Writing Skill product itself is effectively greenfield.

---

## Success Criteria

### User Success

A user achieves success when they can:

1. **Create a named writing profile from examples** — The user can provide several samples, receive a clear style hypothesis, calibrate it, and save a local profile without needing to manually design a full prompt.
2. **Improve the profile through feedback** — The user can grade generated samples with freeform notes and optional numeric ratings, and the skill converts that feedback into more accurate style instructions.
3. **Reuse an approved style by name** — The user can later ask for writing using a saved profile, such as "write this using my `email-professional` style," and get output that follows the saved style without importing unrelated facts from the examples.
4. **Trust privacy-preserving defaults** — The user can inspect the saved profile and see style guidance rather than copied private content, names, work details, or factual claims from source examples.

### Technical Success

The system is successful when:

1. **Profiles are local, structured, and portable** — Each saved profile is a readable file with stable sections for purpose, style traits, structure, defaults, examples, constraints, and invocation guidance.
2. **Settings are explicit and conservative** — A config file stores default behavior, including sanitization and neutral prompts, and risky changes require user confirmation.
3. **Calibration is repeatable enough for evals** — The workflow produces artifacts and examples that can support a regression set for voice match, privacy leakage, and instruction adherence.
4. **Profiles can be forked or extended** — A new profile can start from an existing profile while preserving the relationship and user-visible differences.

### Measurable Outcomes

- A user can create and save a first style profile in 15 minutes or less after providing examples.
- Saved profiles contain no unapproved factual claims, names, private terms, or source-specific details from examples in default mode.
- At least two consecutive calibration outputs receive a user-approved score before a profile is marked ready.
- The initial eval set covers at least four suggested use categories and at least three privacy/adherence failure modes.

---

## User Journeys

### Journey 1: Carter — Building a Personal Email Style

Carter wants an LLM to write emails that sound like him rather than like generic corporate polish. He starts a new `email-professional` profile, pastes a few prior emails, and expects the skill to extract tone, sentence shape, directness, warmth, and formatting habits without preserving workplace-specific content. The skill summarizes the inferred style, generates neutral email examples, and asks Carter to grade what feels right or wrong. After a few rounds of feedback, Carter approves the profile and saves it locally so future sessions can use `email-professional` as an instruction source.

**Requirements Revealed:** profile creation, example intake, sanitization, style-only extraction, neutral calibration prompts, freeform grading, local profile save, profile invocation.

---

### Journey 2: Carter — Forking a Style for a New Context

Carter already has `email-professional`, but now wants `email-neutral`, a slightly less formal style for routine updates. Instead of starting from scratch, he asks the skill to create a new profile from the existing one. The skill loads the source profile, asks what should change, proposes a diff in tone and structure, then generates comparison samples so Carter can tune the difference. The result is a separate local file that inherits useful guidance without mutating the original style.

**Requirements Revealed:** profile discovery, profile inheritance, style diffing, fork confirmation, comparison examples, local persistence.

---

### Journey 3: A Future User — Creating a Presentation Style

A future user installs the skill and wants help writing presentations that feel concise, spoken, and slide-friendly. They create a `presentation` profile, provide a few examples or notes, and accept the default neutral prompts because they do not have polished samples yet. The skill asks targeted questions about audience, pacing, formatting, and speaker notes, then produces samples for feedback. Once saved, the user can ask for outlines, slide copy, or speaker notes using the profile's "how to write" guidance while supplying the actual topic separately.

**Requirements Revealed:** generic single-user flow, style categories beyond email, optional example-light onboarding, style questions, writing versus rewriting support.

---

### Journey Requirements Summary

| User Type | Key Requirements |
|-----------|------------------|
| **Primary creator/user** | Named local profiles, privacy-preserving example analysis, calibration loop, freeform feedback, profile reuse |
| **Power user** | Configurable defaults, profile inheritance, profile updates, explicit override confirmations |
| **Future generic user** | Clear onboarding, multiple writing categories, neutral prompts, inspectable saved artifacts |

---

## Scope

### MVP — Minimum Viable Product (v1)

**Core Deliverables:**
- Guided creation of named writing-style profiles.
- Intake of user writing examples as source material.
- Default sanitization and style-only extraction that avoids saving private facts from examples.
- Neutral calibration prompts by default, with user-provided calibration prompts allowed after explicit request.
- Iterative calibration loop with generated samples, freeform feedback, optional numeric rating, and revised profile guidance.
- Local profile files for approved styles.
- Local settings/config file for defaults such as sanitization, neutral prompts, profile directory, and confirmation behavior.
- Confirmation prompts before disabling sanitization, retaining domain-specific terms, or using user-provided prompts as persistent profile material.
- Ability to create a new profile from an existing profile.
- Basic invocation guidance for later use, such as "use profile `email-professional` to write or rewrite this."

**Quality Gates:**
- The skill must make the distinction between "how to write" and "what to write" clear in the product flow.
- The skill must not save factual content from examples by default.
- The skill must produce an inspectable profile file before considering a style complete.
- The skill must start with no required built-in profile categories; it may suggest broad starter categories such as `email`, `text`, `report`, and `narrative`, while allowing arbitrary user-defined profile names.
- The skill must include enough eval scaffolding to test style match, privacy leakage, and instruction adherence.

### Growth Features (Post-MVP)

**v2: Profile Management**
- Rename, duplicate, archive, compare, and merge profiles.
- Richer profile inheritance graph and profile version history.
- Commands to tighten, soften, formalize, shorten, or otherwise revise existing profiles.

**v3: Stronger Evals and Automation**
- Automated rubric-based scoring with human override.
- Regression test sets per profile.
- Batch calibration over multiple prompts.
- Privacy scanner for saved profiles and generated outputs.

### Vision (Future)

- A personal writing-style system that can maintain a library of style profiles across many contexts while preserving user control, local inspectability, and privacy boundaries.

---

## Functional Requirements

### 1. Profile Creation and Storage

**FR-1.1:** The skill must let the user create a named writing-style profile.
- The profile name must be user-provided or confirmed before saving.
- The skill may suggest broad starter categories such as email, text, report, and narrative, but these are suggestions only, not required defaults.
- The profile name must support arbitrary user-defined types.

**FR-1.2:** The skill must save approved profiles as local files.
- Each profile file must be readable and editable by the user.
- Each profile must include purpose, intended use, style traits, structure guidance, do/don't rules, privacy notes, calibration status, and invocation examples.

**FR-1.3:** The skill must support creating a new profile from an existing profile.
- The user must choose the source profile.
- The skill must ask what should change and preserve a visible relationship to the source profile.
- The source profile must not be modified unless the user explicitly requests it.

### 2. Example Intake and Style Extraction

**FR-2.1:** The skill must ask the user to provide whatever writing examples they have.
- The skill should support multiple examples in one session.
- The skill should work even when the user has few examples by asking supplemental style questions.

**FR-2.2:** The skill must extract style traits rather than factual content by default.
- Extracted traits may include tone, directness, warmth, sentence length, rhythm, structure, formatting, vocabulary level, transition style, and common rhetorical moves.
- Extracted traits must exclude private facts, names, project details, claims, client information, internal terminology, or domain details unless explicitly approved.

**FR-2.3:** The skill must show the user an initial style hypothesis before calibration.
- The hypothesis should be inspectable and editable.
- The user must be able to correct mistaken style assumptions before generated calibration samples are treated as meaningful.

### 3. Privacy and Sanitization Defaults

**FR-3.1:** The skill must default to a sanitization pass for user-provided examples.
- The sanitization pass should identify private or source-specific content and convert it into style-neutral notes.
- The skill must state that examples are being used for style, not retained as content.

**FR-3.2:** The skill must require confirmation before saving source-derived facts or recurring terms.
- If the model believes a term may be part of style rather than content, it must ask the user before retaining it.
- The confirmation should explain the risk of embedding private context into future outputs.

**FR-3.3:** The skill must allow settings overrides while warning the user.
- Overrides may include disabling sanitization, allowing persistent domain terminology, or using user-provided prompts as defaults.
- Riskier settings must require follow-up confirmation.

### 4. Calibration Loop

**FR-4.1:** The skill must generate calibration examples from neutral prompts by default.
- Neutral prompts should avoid copying the user's private topics, workplace details, or personal facts.
- The user may request custom prompts for calibration.

**FR-4.2:** The skill must collect feedback on generated examples.
- Feedback can be freeform.
- The skill should offer optional feedback modes, including pass/fail, numeric rating, rubric-based comments, or "what feels wrong/right."

**FR-4.3:** The skill must revise the profile based on user feedback.
- Revisions should update explicit profile instructions rather than merely noting feedback history.
- The skill should summarize what changed between calibration rounds.

**FR-4.4:** The skill must define when a profile is ready.
- By default, readiness requires user approval and at least two consecutive acceptable calibration outputs.
- The user may manually save a profile earlier with an "experimental" status.

### 5. Reuse and Invocation

**FR-5.1:** The skill must provide instructions for using a saved profile later.
- Invocation guidance should explain how to use the profile for new writing.
- Invocation guidance should explain how to use the profile for rewriting existing drafts.

**FR-5.2:** The skill must keep style separate from task content.
- Saved profiles should describe how to write.
- The user must provide what to write at invocation time unless a specific profile intentionally includes allowed reusable content.

**FR-5.3:** The skill must support profile updates after initial save.
- The user can add examples, adjust style guidance, or recalibrate a profile.
- Updates should preserve prior profile content unless explicitly replaced.

### 6. Settings and Defaults

**FR-6.1:** The skill must maintain a local settings/config file.
- Settings should include default profile directory, sanitization default, calibration prompt mode, confirmation requirements, and readiness criteria.

**FR-6.2:** The skill must explain when a setting changes behavior or privacy risk.
- The user should not be able to accidentally disable privacy-preserving defaults without a clear confirmation step.

### 7. Evals

**FR-7.1:** The initiative must include an eval spec for the Writing Skill.
- The eval spec should cover style match, privacy leakage, instruction adherence, profile persistence, and profile inheritance.

**FR-7.2:** The skill must produce or preserve artifacts useful for evals.
- Example artifacts may include neutral prompts, expected style traits, approved profile snippets, and failure cases.

---

## Non-Functional Requirements

- **Performance:** A normal calibration round should be short enough to feel conversational; target one generated sample and profile revision per user response, with no unnecessary multi-step delays.
- **Reliability:** The workflow should be resumable from local files. If a session is interrupted, the user should be able to inspect the latest draft profile and continue calibration.
- **Security and Privacy:** The default behavior must avoid saving private factual content from writing examples. Profiles and settings are local files; no remote persistence should be assumed or introduced without explicit future design.
- **Maintainability:** Profile files, settings, and eval artifacts should use simple, readable formats. The implementation should keep profile structure, calibration prompts, and privacy rules easy to test and revise.
- **Extensibility:** The system should support arbitrary profile names and future profile-management commands without requiring hard-coded style categories.

---

## Open Questions

- What exact local directory structure should profiles and settings use? Proposed default: `writing-skill/profiles/{profile-name}.md` and `writing-skill/config.json`.
- Should saved profiles include sanitized example excerpts, or only abstracted style rules and generated calibration examples?
- Should profile invocation be a separate command flow in v1, or should v1 only produce reusable profile files and examples of how to invoke them?
- What numeric rating threshold should count as passing if the user gives a score? Proposed default: 4 out of 5 or higher.
- How much of the eval suite should be automated in v1 versus written as human-review scenarios?

---

## Risk Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| The skill saves private facts from examples as "style" | Medium | High | Default sanitization, explicit style/content separation, user confirmation before retaining source-derived terms, profile inspection before save |
| Generated writing feels generically polished instead of user-specific | High | High | Calibration loop, freeform feedback, neutral prompts, style hypothesis review, readiness gate requiring consecutive approved outputs |
| Profiles become vague and hard to reuse | Medium | Medium | Structured profile template with required sections, invocation examples, do/don't rules, and calibration status |
| User over-customizes risky settings without understanding consequences | Medium | Medium | Conservative defaults, risk disclaimers, follow-up confirmation for privacy-affecting changes |
| Scope expands into a full writing application | Medium | Medium | Keep MVP focused on creating, saving, updating, and invoking style profiles; defer full writing workspace and advanced management features |
| Evals are too subjective to be useful | Medium | Medium | Combine human grading with repeatable neutral prompts, privacy/adherence checks, and explicit style traits to evaluate against |
