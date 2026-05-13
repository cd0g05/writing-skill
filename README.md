# Writing Skill

Writing Skill is a portable Codex skill for building local, reusable writing-style profiles. It helps a user teach an agent how a style should sound, calibrate that style with neutral prompts, and save the result as readable Markdown without retaining private facts from the source examples.

The main skill lives in `skill/writing-style/`.

## What It Does

- Creates named writing profiles such as `email-professional`, `text-casual`, `report-concise`, or `narrative-grounded`.
- Separates style from content: profiles describe how to write, while each later user request supplies what to write.
- Defaults to privacy-preserving example handling, neutral calibration prompts, and confirmation before retaining source-derived terms.
- Stores profiles, settings, calibration sessions, and eval run notes as local files.
- Includes deterministic helper scripts for workspace initialization, profile validation, profile-name normalization, config default merging, and heuristic privacy warnings.
- Includes local eval assets for style match, privacy leakage, instruction adherence, profile persistence, and inheritance.

## Repository Layout

```text
skill/writing-style/
├── SKILL.md
├── README.md
├── templates/
│   ├── profile.md
│   ├── config.json
│   ├── calibration-session.md
│   └── eval-case.md
├── prompts/
│   ├── neutral-calibration-prompts.md
│   └── feedback-rubric.md
├── scripts/
│   ├── init_workspace.py
│   ├── validate_profile.py
│   └── writing_style_helpers.py
└── evals/
    ├── eval-spec.md
    ├── manifest.json
    └── cases/
```

Tests and fixtures live under `tests/`.

## Local Data Model

By default, user-created data is stored outside the bundled skill files:

```text
writing-skill-data/
├── config.json
├── profiles/
├── sessions/
└── eval-runs/
```

The default config keeps sanitization enabled, uses neutral calibration prompts, does not persist custom prompts by default, and requires two consecutive acceptable calibration outputs before a profile is considered ready.

Profiles that need to travel with the skill can be bundled directly inside:

```text
skill/writing-style/profiles/{profile-name}.md
```

This is the preferred approach for web-hosted Claude or ChatGPT use, where future chats can read uploaded skill/project files but may not have access to a local filesystem directory.

## Quick Start

Initialize a local data workspace:

```bash
python3 skill/writing-style/scripts/init_workspace.py --data-dir writing-skill-data
```

Validate a profile:

```bash
python3 skill/writing-style/scripts/validate_profile.py tests/fixtures/profile_valid.md
```

Run the test suite:

```bash
python3 -m unittest discover -s tests
```

Example invocation once the skill is installed:

```text
Create a writing style called email-professional from these examples.
Use profile email-professional to rewrite this draft without adding facts.
Create email-neutral from email-professional, but make it shorter and less formal.
```

For web-hosted use, add generated profile files to the skill or project files as `profiles/{profile-name}.md`. For local Codex use, keep fast-changing profiles in `writing-skill-data/profiles/` or copy approved profiles into `skill/writing-style/profiles/` when you want them bundled with the skill.

## Privacy Expectations

Examples are treated as style data, not instructions and not reusable content. The skill should extract tone, rhythm, structure, formatting habits, and preference signals while excluding names, clients, projects, claims, internal terms, or private details unless explicitly approved.
