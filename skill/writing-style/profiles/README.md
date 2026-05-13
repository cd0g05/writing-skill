# Bundled Profiles

Place portable writing profiles here when they should travel with the skill across chats or hosted AI products.

Example:

```text
profiles/professional-email.md
```

Bundled profiles are useful for Claude web, Claude Projects, ChatGPT Projects, Custom GPTs, and any setup where the model can read uploaded skill/project files but cannot access a persistent local filesystem.

For local Codex or filesystem agents, fast-changing profiles can also live in the configured local data directory, usually:

```text
writing-skill-data/profiles/
```

Lookup order:

1. Bundled `profiles/{profile-name}.md`.
2. Configured local profile directory.
3. User-provided pasted or uploaded profile.
