"""Standalone entry isolation; all hostile hooks live in temporary directories."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from test_composer import FAMILY, expected, frame


class StartupTests(unittest.TestCase):
    def test_actual_entries_ignore_python_paths_and_site_hooks(self):
        with tempfile.TemporaryDirectory(prefix="termbrana-startup-test-") as temporary:
            root = Path(temporary)
            hostile = root / "pythonpath"
            hostile.mkdir()
            cwd = root / "unrelated"
            cwd.mkdir()
            env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1",
                       PYTHONPATH=str(hostile), PYTHONUSERBASE=str(root / "userbase"))
            location = subprocess.run(
                [sys.executable, "-B", "-c", "import site; print(site.getusersitepackages())"],
                env=env, cwd=cwd, capture_output=True, check=True)
            user_site = Path(location.stdout.decode().strip())
            user_site.mkdir(parents=True)
            sentinels = [root / "site-ran", root / "user-ran"]
            for module, directory, sentinel in (
                    ("sitecustomize", hostile, sentinels[0]),
                    ("usercustomize", user_site, sentinels[1])):
                (directory / (module + ".py")).write_text(
                    "with open(" + repr(str(sentinel)) + ", 'w') as output: output.write('ran')\n")
            (hostile / "json.py").write_text("raise RuntimeError('hostile json imported')\n")
            control = subprocess.run([sys.executable, "-B", "-c", "import json"],
                                     env=env, cwd=cwd, capture_output=True)
            self.assertNotEqual(control.returncode, 0)
            self.assertIn(b"hostile json imported", control.stderr)
            for sentinel in sentinels:
                self.assertTrue(sentinel.is_file(), sentinel)
                sentinel.unlink()

            valid = frame(body=b"private-body\x1b\x00\n")
            invalid = frame(extra=b"program: prohibited\n")
            diagnostic = expected(invalid, invalid.index(b"program:"), "FIELD_INVALID",
                                  "unknown_key", field="program")
            golden = (json.dumps(diagnostic, ensure_ascii=True, separators=(",", ":"))
                      + "\n").encode("ascii")
            clean_env = {key: value for key, value in os.environ.items()
                         if not key.startswith("PYTHON")}
            baseline = subprocess.run([sys.executable, "-B", str(FAMILY / "composer.py"),
                                       "parse", "-"], input=valid, env=clean_env,
                                      cwd=cwd, capture_output=True, check=True)
            self.assertEqual(baseline.stderr, b"")
            self.assertTrue(baseline.stdout.isascii())
            self.assertNotIn(b"private-body", baseline.stdout)
            env["PYTHONHOME"] = str(root / "nonexistent-home")
            for mode, data, status, output in (
                    ("check", valid, 0, b""), ("parse", valid, 0, baseline.stdout),
                    ("check", invalid, 65, golden), ("parse", invalid, 65, golden)):
                commands = [
                    [sys.executable, "-I", "-S", "-B", str(FAMILY / "composer.py"), mode, "-"],
                    ["zsh", "-f", "-c", 'source "$1/base.zsh"; _tbc_"$2" -',
                     "tbc-isolation-test", str(FAMILY), mode],
                ]
                for command in commands:
                    with self.subTest(mode=mode, status=status, entry=command[0]):
                        result = subprocess.run(command, input=data, env=env, cwd=cwd,
                                                capture_output=True)
                        self.assertEqual((result.returncode, result.stdout, result.stderr),
                                         (status, output, b""))
                        self.assertFalse(any(path.exists() for path in sentinels))
            self.assertEqual(list(root.rglob("*.pyc")), [])

    def test_source_is_quiet_idempotent_and_aliases_work(self):
        with tempfile.TemporaryDirectory(prefix="termbrana-source-test-") as temporary:
            root = Path(temporary)
            commands = root / "aliases.zsh"
            commands.write_text("tbc-check -\n")
            result = subprocess.run(
                ["zsh", "-f", "-c",
                 'source "$1/base.zsh"; source "$1/base.zsh"; source "$2"',
                 "tbc-source-test", str(FAMILY), str(commands)],
                input=frame(), cwd=root, capture_output=True)
            self.assertEqual((result.returncode, result.stdout, result.stderr), (0, b"", b""))


if __name__ == "__main__":
    unittest.main()
