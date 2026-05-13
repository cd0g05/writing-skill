"""Deterministic helpers for Writing Style local artifacts."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any


DEFAULT_CONFIG: dict[str, Any] = {
    "version": 1,
    "bundled_profile_directory": "profiles",
    "profile_directory": "writing-skill-data/profiles",
    "session_directory": "writing-skill-data/sessions",
    "eval_run_directory": "writing-skill-data/eval-runs",
    "sanitization": {
        "enabled": True,
        "require_confirmation_to_disable": True,
        "require_confirmation_for_source_terms": True,
    },
    "calibration": {
        "default_prompt_mode": "neutral",
        "allow_custom_prompts": True,
        "save_custom_prompts_by_default": False,
        "readiness": {
            "minimum_consecutive_passes": 2,
            "passing_numeric_score": 4,
        },
    },
    "profiles": {
        "default_status": "draft",
        "allow_inheritance": True,
        "name_format": "kebab-case",
    },
}

REQUIRED_FRONT_MATTER = {
    "profile_name",
    "version",
    "status",
    "created_at",
    "updated_at",
    "source_profile",
    "privacy_mode",
    "sanitization_enabled",
    "allowed_source_terms",
    "calibration",
}

REQUIRED_HEADINGS = [
    "# Writing Profile:",
    "## Purpose and Use Cases",
    "## Style Traits",
    "## Structure and Formatting",
    "## Do / Do Not Rules",
    "## Privacy and Content Boundaries",
    "## Calibration Summary",
    "## Invocation Examples",
    "## Change Notes",
]

VALID_STATUSES = {"draft", "experimental", "ready"}
DISALLOWED_PRIVACY_TERMS = [
    "acme corp",
    "client name",
    "confidential",
    "internal project",
    "ssn",
    "social security",
    "api key",
    "password",
    "private roadmap",
]


def normalize_profile_name(raw_name: str) -> str:
    """Return recommended kebab-case profile name or raise ValueError."""
    cleaned = raw_name.strip().lower()
    if not cleaned:
        raise ValueError("Profile name cannot be empty.")
    cleaned = re.sub(r"['\"]", "", cleaned)
    cleaned = re.sub(r"[^a-z0-9]+", "-", cleaned).strip("-")
    cleaned = re.sub(r"-{2,}", "-", cleaned)
    if not cleaned:
        raise ValueError("Profile name must contain at least one letter or number.")
    if len(cleaned) > 80:
        raise ValueError("Profile name must be 80 characters or fewer.")
    return cleaned


def deep_merge_defaults(existing: dict[str, Any], defaults: dict[str, Any]) -> dict[str, Any]:
    """Merge missing defaults into existing config without dropping unknown keys."""
    merged = deepcopy(existing)
    for key, value in defaults.items():
        if key not in merged:
            merged[key] = deepcopy(value)
        elif isinstance(value, dict) and isinstance(merged[key], dict):
            merged[key] = deep_merge_defaults(merged[key], value)
    return merged


def load_config(path: Path) -> dict[str, Any]:
    """Load config, applying defaults without dropping unknown keys."""
    if not path.exists():
        return deepcopy(DEFAULT_CONFIG)
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object.")
    return deep_merge_defaults(data, DEFAULT_CONFIG)


def split_front_matter(text: str) -> tuple[dict[str, Any], str]:
    """Parse a small YAML-front-matter subset used by Writing Style profiles."""
    if not text.startswith("---\n"):
        raise ValueError("Missing YAML front matter delimited by '---'.")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("Missing closing YAML front matter delimiter.")
    raw = text[4:end]
    body = text[end + 5 :]
    parsed: dict[str, Any] = {}
    current_parent: str | None = None
    for line in raw.splitlines():
        if not line.strip():
            continue
        if line.startswith("  ") and current_parent:
            child_key, _, child_value = line.strip().partition(":")
            parsed.setdefault(current_parent, {})[child_key] = _parse_scalar(child_value.strip())
            continue
        key, sep, value = line.partition(":")
        if not sep:
            continue
        key = key.strip()
        value = value.strip()
        if value == "":
            parsed[key] = {}
            current_parent = key
        else:
            parsed[key] = _parse_scalar(value)
            current_parent = None
    return parsed, body


def _parse_scalar(value: str) -> Any:
    if value in {"null", "Null", "NULL"}:
        return None
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if value == "[]":
        return []
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    try:
        return int(value)
    except ValueError:
        return value


def validate_profile(path: Path) -> list[str]:
    """Return validation errors; empty list means structurally valid."""
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    try:
        metadata, body = split_front_matter(text)
    except ValueError as exc:
        return [f"{path}: {exc}"]

    missing = sorted(REQUIRED_FRONT_MATTER - set(metadata))
    for key in missing:
        errors.append(f"{path}: missing front matter field '{key}'.")

    status = metadata.get("status")
    if status is not None and status not in VALID_STATUSES:
        errors.append(f"{path}: status must be one of {sorted(VALID_STATUSES)}.")

    calibration = metadata.get("calibration")
    if calibration is not None and not isinstance(calibration, dict):
        errors.append(f"{path}: calibration front matter must be a mapping.")

    for heading in REQUIRED_HEADINGS:
        if heading == "# Writing Profile:":
            if not any(line.startswith(heading) for line in body.splitlines()):
                errors.append(f"{path}: missing heading starting with '{heading}'.")
        elif heading not in body:
            errors.append(f"{path}: missing heading '{heading}'.")
    return errors


def scan_profile_privacy_risks(path: Path) -> list[str]:
    """Return heuristic warnings for possible retained source-specific content."""
    text = path.read_text(encoding="utf-8").lower()
    warnings = []
    for term in DISALLOWED_PRIVACY_TERMS:
        if term in text:
            warnings.append(f"{path}: possible private/source-specific term: '{term}'.")
    return warnings
