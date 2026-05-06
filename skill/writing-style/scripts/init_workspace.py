#!/usr/bin/env python3
"""Initialize a local Writing Style data workspace."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from writing_style_helpers import DEFAULT_CONFIG


def init_workspace(data_dir: Path, *, force: bool = False) -> list[Path]:
    data_dir.mkdir(parents=True, exist_ok=True)
    created_or_updated: list[Path] = []

    for child in ["profiles", "sessions", "eval-runs"]:
        path = data_dir / child
        path.mkdir(parents=True, exist_ok=True)
        created_or_updated.append(path)

    config_path = data_dir / "config.json"
    config = DEFAULT_CONFIG.copy()
    config["profile_directory"] = str(data_dir / "profiles")
    config["session_directory"] = str(data_dir / "sessions")
    config["eval_run_directory"] = str(data_dir / "eval-runs")

    if config_path.exists() and not force:
        return created_or_updated

    config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    created_or_updated.append(config_path)
    return created_or_updated


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize Writing Style local data folders.")
    parser.add_argument("--data-dir", default="writing-skill-data", help="Directory for config, profiles, sessions, and eval runs.")
    parser.add_argument("--force", action="store_true", help="Overwrite config.json if it already exists.")
    args = parser.parse_args()

    try:
        changed = init_workspace(Path(args.data_dir), force=args.force)
    except OSError as exc:
        print(f"Could not initialize workspace at {args.data_dir}: {exc}", file=sys.stderr)
        return 2

    print("Writing Style workspace is ready.")
    for path in changed:
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
