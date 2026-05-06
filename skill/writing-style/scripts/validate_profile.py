#!/usr/bin/env python3
"""Validate Writing Style profile artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from writing_style_helpers import scan_profile_privacy_risks, validate_profile


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Writing Style profile Markdown file.")
    parser.add_argument("profile_path", help="Path to the profile Markdown file.")
    parser.add_argument("--privacy-scan", action="store_true", help="Run heuristic private/source-specific term warnings.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable validation results.")
    args = parser.parse_args()

    path = Path(args.profile_path)
    try:
        errors = validate_profile(path)
        warnings = scan_profile_privacy_risks(path) if args.privacy_scan else []
    except OSError as exc:
        message = f"Could not read {path}: {exc}"
        if args.json:
            print(json.dumps({"ok": False, "errors": [message], "warnings": []}, indent=2))
        else:
            print(message, file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps({"ok": not errors, "errors": errors, "warnings": warnings}, indent=2))
    else:
        for error in errors:
            print(f"- {error}")
        for warning in warnings:
            print(f"- warning: {warning}")
        if not errors:
            print(f"Profile is valid: {path}")
        if args.privacy_scan:
            print("Privacy scan is heuristic and does not prove the profile is free of private content.")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
