---
summary: "Writing Skill will be implemented as a portable Codex skill with Markdown-first instructions, local profile files, conservative JSON settings, reusable neutral calibration prompts, and a small Python helper layer for validation/sanitization support where deterministic checks are useful. The architecture avoids a database, web app, or remote storage; profiles remain inspectable local artifacts, privacy-preserving defaults are enforced by skill workflow and config, and evals are represented as repeatable local cases plus human-review rubrics."
phase: "tech"
when_to_load:
  - "When implementing or reviewing Writing Skill architecture, interfaces, data models, conventions, and sequencing."
  - "When checking whether changes still conform to the agreed technical approach for local profiles, privacy defaults, calibration, and evals."
depends_on:
  - "prd.md"
  - "ux.md"
modules:
  - "skill/writing-style/SKILL.md"
  - "skill/writing-style/templates/"
  - "skill/writing-style/prompts/"
  - "skill/writing-style/scripts/"
  - "skill/writing-style/evals/"
index:
  overview: "## Overview & Context"
  stack: "## Tech Stack & Dependencies"
  structure: "## Project / Module Structure"
  adrs: "## Architecture Decisions (ADRs)"
  data_models: "## Data Models"
  interfaces: "## API & Interface Design"
  conventions: "## Implementation Patterns & Conventions"
  security_performance: "## Security & Performance"
  implementation_sequence: "## Implementation Sequence"
next_section: "Approach"
---

# Tech Design: Writing Skill

## Progress

- [x] Overview & Context
- [x] Tech Stack & Dependencies
- [x] Project / Module Structure
- [x] Architecture Decisions (ADRs)
- [x] Data Models
- [x] API & Interface Design
- [x] Implementation Patterns & Conventions
- [x] Security & Performance
- [x] Implementation Sequence

---

## Overview & Context

**Summary:** Writing Skill is a portable agent skill, not a standalone application. The core implementation is an instruction-driven workflow in `SKILL.md` plus bundled templates, neutral calibration prompt sets, profile schemas, eval cases, and optional Python helper scripts for validation and local artifact operations. The system stores durable state in local Markdown and JSON files so users can inspect, edit, version, and reuse their writing profiles without hidden persistence.

The architecture should keep the LLM responsible for coaching, style interpretation, and iterative calibration, while deterministic helper code handles file shape validation, config defaults, profile naming, and privacy-oriented lint checks. This avoids pretending that style learning can be fully automated while still giving the skill reliable structure.

### Cross-Cutting Concerns

1. **Privacy by default** — The skill must never save source-derived facts, names, private details, or domain terms unless the user explicitly confirms they are reusable style material.
2. **Local inspectability** — All durable outputs must be local, readable files; no hidden database or remote service is introduced in MVP.
3. **Style/content separation** — Profiles describe how to write. The user's later writing task supplies what to write.
4. **Resumability** — In-progress and saved profile files must contain enough state for a later session to continue calibration.
5. **Portable skill packaging** — The skill should be usable as a self-contained directory that can be installed into a Codex skills location later.
6. **Eval readiness** — Calibration prompts, profile templates, and eval cases should be structured enough to support repeatable human or automated review.

### Brownfield Notes

The repository is currently a minimal Python project with Cicadas artifacts and no product code beyond `main.py`. There is no existing canon, product UI, database, or application framework to preserve. The implementation should avoid introducing a web framework, database, or dependency-heavy stack unless later requirements prove they are necessary.

---

## Tech Stack & Dependencies

| Category | Selection | Rationale |
|----------|-----------|-----------|
| **Language/Runtime** | Markdown instructions plus Python 3.12 helper scripts | Agent skills are instruction-first; Python is already the repo runtime and is enough for validation helpers. |
| **Framework** | None | A framework would add complexity without improving the conversational skill workflow. |
| **Database** | None | Local Markdown/JSON artifacts meet the profile persistence requirement and remain inspectable. |
| **Serialization** | JSON for config/metadata; Markdown with YAML front matter for profiles | JSON is simple for settings; Markdown is readable for style profiles. |
| **Testing** | `pytest` if helper scripts grow beyond trivial logic; otherwise script-level fixture tests | Deterministic helper functions need tests; pure instruction docs need eval cases and validation. |
| **Key Libraries** | Standard library only for MVP | Keeps the skill portable and easy to install. |

**New dependencies introduced:**
- None for MVP.

**Dependencies explicitly rejected:**
- `pydantic` — Useful for schema validation, but unnecessary unless profile/config validation becomes complex.
- `click` or `typer` — Helpful for CLIs, but MVP helper scripts can use `argparse` or simple command interfaces.
- SQLite or other databases — Would hide data and overbuild local profile storage.
- Web/frontend frameworks — The MVP surface is agent conversation plus local files, not a UI application.

---

## Project / Module Structure

```text
writing-skill/
├── README.md                         # [MODIFIED] Product overview and usage notes
├── pyproject.toml                    # [MODIFIED] Project metadata; optional test dependency if needed
├── main.py                           # [MODIFIED/OPTIONAL] Remove or replace placeholder with helper entrypoint only if useful
├── skill/
│   └── writing-style/
│       ├── SKILL.md                  # Core agent skill instructions and trigger guidance
│       ├── templates/
│       │   ├── profile.md            # Saved style profile template
│       │   ├── config.json           # Default settings template
│       │   ├── calibration-session.md # Optional in-progress session template
│       │   └── eval-case.md          # Eval case template
│       ├── prompts/
│       │   ├── neutral-calibration-prompts.md # Default neutral prompt bank
│       │   └── feedback-rubric.md    # Human grading/rubric guidance
│       ├── scripts/
│       │   ├── validate_profile.py   # Checks profile shape and risky content flags
│       │   └── init_workspace.py     # Creates local profile/config folders from templates
│       └── evals/
│           ├── eval-spec.md          # Eval plan generated during/after tech design
│           └── cases/
│               └── README.md         # How to add repeatable eval cases
└── tests/
    ├── test_validate_profile.py      # Deterministic helper tests
    └── fixtures/
        ├── profile_valid.md
        └── profile_privacy_flags.md
```

**User-created local workspace default:**

```text
writing-skill-data/
├── config.json
├── profiles/
│   └── {profile-name}.md
├── sessions/
│   └── {profile-name}-{timestamp}.md
└── eval-runs/
```

**Key structural decisions:**
- The product skill lives under `skill/writing-style/` so it can later be published or installed as a portable skill directory.
- Bundled templates/prompts live with the skill; user-created profiles live in a separate configurable data directory.
- Helper scripts must not be required for the conversational workflow unless they provide deterministic value.
- Eval artifacts live with the skill for reusable cases, while run outputs live in user data.

---

## Architecture Decisions (ADRs)

### ADR-1: Implement as a Portable Agent Skill, Not a Web App

**Decision:** Build Writing Skill as a Codex-compatible skill directory centered on `SKILL.md`, bundled templates, prompt banks, helper scripts, and eval cases.

**Rationale:** The required interaction is conversational and agent-mediated. A web app would add UI, persistence, and distribution work before the core style-calibration workflow is proven.

**Alternatives rejected:** A CLI-only tool would be too rigid for nuanced style feedback. A web app would be overbuilt for a local personal workflow. A pure prompt file would not provide enough artifact structure, validation, or eval support.

**Consequences:** The skill depends on host-agent capabilities for conversation and file edits. In return, it stays portable and easy to iterate.

**Affects:** `skill/writing-style/SKILL.md`, `templates/`, `prompts/`, `README.md`.

---

### ADR-2: Store Profiles as Markdown With YAML Front Matter

**Decision:** Save each writing profile as a local Markdown file with structured YAML front matter and standard body sections.

**Rationale:** Profiles are meant to be read, edited, and reused by humans and agents. Markdown gives the user a pleasant artifact, while front matter gives scripts and agents stable metadata.

**Alternatives rejected:** JSON-only profiles are easy to parse but unpleasant to edit and review. Freeform Markdown is readable but too inconsistent for validation and reuse. A database hides the product's most important artifact.

**Consequences:** Validation must tolerate Markdown structure while enforcing required headings and metadata. Implementors should keep parsing simple and avoid brittle line-number assumptions.

**Affects:** `templates/profile.md`, `scripts/validate_profile.py`, eval cases, profile-loading instructions in `SKILL.md`.

---

### ADR-3: Keep Settings in JSON With Conservative Defaults

**Decision:** Use a local `config.json` for workspace defaults such as profile directory, sanitization mode, neutral prompt mode, readiness threshold, and confirmation requirements.

**Rationale:** Settings affect behavior and privacy; JSON is easy to validate and diff. Defaults should be explicit rather than implicit in a long instruction file.

**Alternatives rejected:** Storing settings only in prose makes behavior harder to test. Environment variables are poor UX for a personal writing workflow. Per-profile-only settings would duplicate global defaults.

**Consequences:** The skill must read existing config before changing settings and must preserve unknown future keys. Privacy-reducing changes need a confirmation step in the skill workflow.

**Affects:** `templates/config.json`, `scripts/init_workspace.py`, `SKILL.md` settings-change flow.

---

### ADR-4: Use LLM Judgment for Style Analysis, Deterministic Checks for Artifact Hygiene

**Decision:** Let the LLM perform style extraction, hypothesis drafting, calibration generation, and feedback interpretation; use helper scripts only for deterministic checks such as profile naming, required sections, config shape, and obvious privacy-risk markers.

**Rationale:** Style interpretation is qualitative and context-sensitive. Deterministic scripts are useful for preventing malformed artifacts but should not pretend to understand voice match.

**Alternatives rejected:** Fully deterministic style extraction would be brittle and underpowered. Fully LLM-only artifact handling would invite inconsistent files and missed validation opportunities.

**Consequences:** Evals must include human-review rubrics for style match and deterministic checks for privacy leakage and file structure.

**Affects:** `SKILL.md`, `scripts/validate_profile.py`, `prompts/feedback-rubric.md`, `evals/`.

---

### ADR-5: Default Calibration Uses Neutral Prompt Banks

**Decision:** Calibration examples should default to reusable neutral prompts grouped by writing category. User-provided prompts are allowed, but the skill must clarify whether they are one-time calibration inputs or persistent profile guidance.

**Rationale:** Neutral prompts reduce the chance of copying private sample content into profile behavior and make eval cases repeatable.

**Alternatives rejected:** Always using prompts derived from user examples increases privacy risk. Always requiring user-provided prompts adds friction and weakens onboarding.

**Consequences:** The prompt bank must cover core categories well enough for MVP and be easy to extend. The skill must clearly label custom prompts and avoid saving them as defaults unless confirmed.

**Affects:** `prompts/neutral-calibration-prompts.md`, `SKILL.md` calibration flow, eval prompt sets.

---

### ADR-6: Treat Evals as First-Class Local Artifacts

**Decision:** Create an eval spec and local eval case templates as part of the initiative, with cases for style match, privacy leakage, instruction adherence, profile persistence, and profile inheritance.

**Rationale:** The product is LLM-powered and quality is subjective unless the expected behavior is made repeatable. Evals do not need a hosted runner in MVP, but the cases and rubric must exist.

**Alternatives rejected:** Deferring evals entirely would make regressions invisible. Building a full automated eval harness before the skill exists would slow iteration.

**Consequences:** The Approach phase must decide whether eval implementation happens before build or in parallel. MVP can start with human-review cases and deterministic artifact checks.

**Affects:** `evals/eval-spec.md`, `evals/cases/`, `prompts/feedback-rubric.md`, tests.

---

## Data Models

### `config.json`

```json
{
  "version": 1,
  "profile_directory": "writing-skill-data/profiles",
  "session_directory": "writing-skill-data/sessions",
  "sanitization": {
    "enabled": true,
    "require_confirmation_to_disable": true,
    "require_confirmation_for_source_terms": true
  },
  "calibration": {
    "default_prompt_mode": "neutral",
    "allow_custom_prompts": true,
    "save_custom_prompts_by_default": false,
    "readiness": {
      "minimum_consecutive_passes": 2,
      "passing_numeric_score": 4
    }
  },
  "profiles": {
    "default_status": "draft",
    "allow_inheritance": true,
    "name_format": "kebab-case"
  }
}
```

**Key field decisions:**
- `version` — Enables future migrations.
- `sanitization.enabled` — Defaults true to satisfy privacy requirements.
- `save_custom_prompts_by_default` — Defaults false to keep user prompts from silently becoming persistent profile context.
- `minimum_consecutive_passes` — Encodes the readiness rule from the PRD.

### Profile Front Matter

```yaml
profile_name: "email-professional"
version: 1
status: "draft|experimental|ready"
created_at: "YYYY-MM-DD"
updated_at: "YYYY-MM-DD"
source_profile: null
privacy_mode: "style_only"
sanitization_enabled: true
allowed_source_terms: []
calibration:
  consecutive_passes: 0
  passing_numeric_score: 4
  last_score: null
  last_feedback_summary: ""
```

### Profile Body Sections

```markdown
# Writing Profile: email-professional

## Purpose and Use Cases
## Style Traits
## Structure and Formatting
## Do / Do Not Rules
## Privacy and Content Boundaries
## Calibration Summary
## Invocation Examples
## Change Notes
```

### Calibration Session

```yaml
session_id: "email-professional-YYYYMMDD-HHMM"
profile_name: "email-professional"
status: "in_progress|completed|abandoned"
prompt_mode: "neutral|custom"
privacy_mode: "style_only"
```

Body sections:

```markdown
## Source Example Summary
## Sanitization Notes
## Style Hypothesis
## Calibration Rounds
## Pending Decisions
```

### Eval Case

```yaml
case_id: "style-email-professional-001"
category: "style_match|privacy_leakage|instruction_adherence|profile_persistence|inheritance"
profile_fixture: "profiles/email-professional.md"
prompt_fixture: "prompts/email-neutral-001.md"
expected_result_type: "human_rubric|deterministic_check"
```

Body sections:

```markdown
## User Prompt
## Expected Style Signals
## Must Not Include
## Rubric
## Passing Criteria
```

### Modified Models

No existing product models are modified. All models are additive local artifacts.

### Schema / Migration Notes

MVP starts at schema `version: 1`. Future migrations should be explicit helper commands or documented manual migrations; profile files should never be silently rewritten without showing a diff or summary.

---

## API & Interface Design

### Conversational Commands

These are natural-language command patterns handled by `SKILL.md`, not shell commands:

```text
Create a writing style called {profile-name}
Create {new-profile} from {source-profile}
Update/recalibrate {profile-name}
Use {profile-name} to write {task}
Use {profile-name} to rewrite this draft: {draft}
List writing profiles
Show settings
Change setting {setting-name} to {value}
```

### Helper Script Interfaces

```text
python3 skill/writing-style/scripts/init_workspace.py [--data-dir writing-skill-data]
```

Creates the user data directory and default config if missing. It must not overwrite existing config or profiles without explicit `--force`.

```text
python3 skill/writing-style/scripts/validate_profile.py {profile_path}
```

Validates required front matter and headings. Returns nonzero on structural failure and prints actionable messages.

Optional later flags:

```text
python3 skill/writing-style/scripts/validate_profile.py {profile_path} --privacy-scan
python3 skill/writing-style/scripts/validate_profile.py {profile_path} --json
```

### Interface Contracts

Helper scripts should expose importable pure functions for tests:

```python
from pathlib import Path
from typing import Any


def normalize_profile_name(raw_name: str) -> str:
    """Return recommended kebab-case profile name or raise ValueError."""


def load_config(path: Path) -> dict[str, Any]:
    """Load config, applying defaults without dropping unknown keys."""


def validate_profile(path: Path) -> list[str]:
    """Return validation errors; empty list means structurally valid."""


def scan_profile_privacy_risks(path: Path) -> list[str]:
    """Return heuristic warnings for possible retained source-specific content."""
```

### Backward Compatibility

There are no existing profiles to preserve. Once profile schema `version: 1` ships, later changes must either remain backward-compatible or provide migration guidance.

---

## Implementation Patterns & Conventions

### Naming Conventions

| Construct | Convention | Example |
|-----------|------------|---------|
| Profile names | lowercase kebab-case | `email-professional` |
| Python functions | snake_case | `validate_profile()` |
| Python files | snake_case | `validate_profile.py` |
| Markdown templates | kebab-case | `calibration-session.md` |
| Eval case IDs | category-profile-number | `privacy-email-professional-001` |
| Config keys | snake_case | `profile_directory` |

### Error Handling Pattern

```python
def main() -> int:
    try:
        errors = validate_profile(profile_path)
    except OSError as exc:
        print(f"Could not read {profile_path}: {exc}")
        return 2

    if errors:
        for error in errors:
            print(f"- {error}")
        return 1
    print("Profile is valid.")
    return 0
```

**Rules:**
- User-facing errors must include the file path and the recovery action.
- Helper scripts return `0` for success, `1` for validation failure, and `2` for file/system failure.
- Scripts must not overwrite user files unless a flag explicitly allows it.
- The skill must summarize file changes before writing when privacy or profile behavior changes.

### Testing Pattern

```python
def test_validate_profile_accepts_required_template(tmp_path):
    profile = tmp_path / "email-professional.md"
    profile.write_text(VALID_PROFILE)

    assert validate_profile(profile) == []
```

**Coverage expectations:** 100% of non-trivial helper validation logic should have tests. Skill instruction behavior is covered by eval cases rather than unit tests.

**Mocking strategy:** Prefer temp directories and fixture files over mocks. Avoid network calls entirely.

### Markdown Artifact Conventions

- Required headings must be stable and exact.
- Metadata belongs in YAML front matter; long explanations belong in body sections.
- Profiles should avoid raw source examples by default. If examples are included, they must be generated, sanitized, or explicitly approved.
- Change notes should be concise and user-readable.

---

## Security & Performance

### Security and Privacy

| Concern | Mitigation |
|---------|------------|
| Private facts saved into profiles | Style-only extraction instructions, sanitization pass, privacy-risk confirmations, profile inspection before save |
| Accidental source-term retention | `allowed_source_terms` defaults empty; confirmation required before adding terms |
| Risky settings changes | Config defaults conservative; privacy-reducing changes require explicit confirmation |
| Prompt injection from user examples | Treat examples as data; never follow instructions embedded inside examples |
| File overwrite/data loss | No overwrite by default; summarize changes and require confirmation before replacing profiles/config |
| Hidden persistence | No database or remote storage in MVP; all durable state is local files |

### Performance

| Concern | Target | Approach |
|---------|--------|----------|
| Workspace init | < 1 second for normal local folders | Simple file creation from bundled templates |
| Profile validation | < 1 second per profile for typical Markdown files | Plain text/front matter checks |
| Calibration turn count | 1 generated sample per normal round | Avoid large batch generation unless user requests it |
| File size | Profiles remain human-readable, target < 20 KB each | Summarize feedback; do not store all raw examples |

### Observability

MVP observability is local and artifact-based:
- **Profile change notes:** record meaningful style/profile changes.
- **Calibration summaries:** record feedback summaries and readiness status.
- **Eval run notes:** store human-review outcomes in `writing-skill-data/eval-runs/` if eval execution is included.

No telemetry, analytics, or remote logging should be introduced.

---

## Implementation Sequence

1. **Skill scaffold** *(blocking)* — Create `skill/writing-style/` with `SKILL.md`, profile template, config template, and README usage notes.
2. **Artifact schemas** *(depends on 1)* — Finalize profile, config, calibration session, and eval case templates.
3. **Core workflow instructions** *(depends on 1 and 2)* — Implement create-profile, sanitize/analyze, calibrate, save, fork, invoke, and settings flows in `SKILL.md`.
4. **Neutral prompts and feedback rubric** *(parallel with 3)* — Build default prompt bank and feedback modes for core categories.
5. **Helper scripts** *(depends on 2)* — Add workspace init and profile validation scripts with fixture tests.
6. **Eval spec and cases** *(parallel or before build, decision required in Approach)* — Define style match, privacy leakage, instruction adherence, persistence, and inheritance evals.
7. **Documentation polish** *(depends on 1-6)* — Update README with install/use examples and profile file examples.
8. **Validation pass** *(depends on 1-7)* — Run helper tests, validate bundled templates, and dry-run representative skill workflows.

**Parallel work opportunities:**
- Templates and helper scripts can be built separately once schemas are agreed.
- Neutral prompt bank and eval cases can be drafted in parallel.
- README usage docs can begin after the core IA is stable.

**Known implementation risks:**
- **Profile privacy validation may be heuristic:** deterministic scripts cannot reliably distinguish all private facts from style. Mitigation: rely on default workflow, user inspection, and eval cases rather than claiming perfect scanning.
- **Skill trigger scope may be too broad or too narrow:** the `SKILL.md` description must be tested against representative user requests.
- **Calibration can become tedious:** MVP should generate one sample at a time and offer save-as-experimental to avoid trapping the user in an endless loop.
- **Eval automation may be premature:** Approach should decide whether to implement human-review evals first, then add automation later.
