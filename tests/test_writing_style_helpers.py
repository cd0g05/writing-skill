import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skill" / "writing-style" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from writing_style_helpers import load_config, normalize_profile_name, scan_profile_privacy_risks, validate_profile


class WritingStyleHelperTests(unittest.TestCase):
    def test_normalize_profile_name_recommends_kebab_case(self):
        self.assertEqual(normalize_profile_name(" Email Professional! "), "email-professional")

    def test_normalize_profile_name_rejects_empty(self):
        with self.assertRaises(ValueError):
            normalize_profile_name("!!!")

    def test_load_config_merges_defaults_and_preserves_unknown_keys(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / "config.json"
            config.write_text(json.dumps({"version": 1, "custom_key": {"kept": True}}), encoding="utf-8")

            loaded = load_config(config)

        self.assertEqual(loaded["custom_key"], {"kept": True})
        self.assertIs(loaded["sanitization"]["enabled"], True)
        self.assertEqual(loaded["profiles"]["name_format"], "kebab-case")

    def test_validate_profile_accepts_valid_fixture(self):
        self.assertEqual(validate_profile(ROOT / "tests" / "fixtures" / "profile_valid.md"), [])

    def test_validate_profile_reports_invalid_fixture(self):
        errors = validate_profile(ROOT / "tests" / "fixtures" / "profile_invalid.md")

        self.assertTrue(any("source_profile" in error for error in errors))
        self.assertTrue(any("status must be" in error for error in errors))
        self.assertTrue(any("Style Traits" in error for error in errors))

    def test_privacy_scan_flags_known_terms(self):
        warnings = scan_profile_privacy_risks(ROOT / "tests" / "fixtures" / "profile_privacy_flags.md")

        self.assertTrue(any("acme corp" in warning for warning in warnings))
        self.assertTrue(any("confidential" in warning for warning in warnings))

    def test_init_workspace_creates_directories_and_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_dir = Path(tmp) / "writing-skill-data"
            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "init_workspace.py"), "--data-dir", str(data_dir)],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0)
            self.assertTrue((data_dir / "config.json").exists())
            self.assertTrue((data_dir / "profiles").is_dir())
            self.assertTrue((data_dir / "sessions").is_dir())
            self.assertTrue((data_dir / "eval-runs").is_dir())

    def test_init_workspace_does_not_overwrite_config_without_force(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_dir = Path(tmp) / "writing-skill-data"
            data_dir.mkdir()
            config = data_dir / "config.json"
            config.write_text('{"custom": true}\n', encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "init_workspace.py"), "--data-dir", str(data_dir)],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0)
            self.assertEqual(config.read_text(encoding="utf-8"), '{"custom": true}\n')

    def test_validate_profile_script_exit_codes(self):
        valid = ROOT / "tests" / "fixtures" / "profile_valid.md"
        invalid = ROOT / "tests" / "fixtures" / "profile_invalid.md"
        missing = ROOT / "tests" / "fixtures" / "missing.md"

        ok = subprocess.run(
            [sys.executable, str(SCRIPTS / "validate_profile.py"), str(valid)],
            text=True,
            capture_output=True,
            check=False,
        )
        bad = subprocess.run(
            [sys.executable, str(SCRIPTS / "validate_profile.py"), str(invalid)],
            text=True,
            capture_output=True,
            check=False,
        )
        system = subprocess.run(
            [sys.executable, str(SCRIPTS / "validate_profile.py"), str(missing)],
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(ok.returncode, 0)
        self.assertEqual(bad.returncode, 1)
        self.assertEqual(system.returncode, 2)


if __name__ == "__main__":
    unittest.main()
