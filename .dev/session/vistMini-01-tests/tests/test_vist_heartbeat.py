#!/usr/bin/env python3
import importlib.util
import json
import os
import stat
import subprocess
import tempfile
import unittest
from unittest import mock
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts" / "vist-heartbeat.py"
SPEC = importlib.util.spec_from_file_location("vist_heartbeat", SCRIPT)
heartbeat = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(heartbeat)


class HeartbeatTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.bed = self.root / "bed"; self.bed.mkdir()
        self.calls = self.root / "calls"
        self.codex = self.program("codex", f"#!/bin/sh\nprintf 'queue %s\\n' \"$*\" >> {self.calls}\nexit ${{QUEUE_EXIT:-0}}\n")
        self.systemctl = self.program("systemctl", f"#!/bin/sh\nprintf 'stop %s\\n' \"$*\" >> {self.calls}\nexit 0\n")
        self.lease_path = self.root / "lease.json"

    def tearDown(self): self.temp.cleanup()

    def program(self, name, body):
        path = self.root / name; path.write_text(body); path.chmod(stat.S_IRWXU); return str(path)

    def lease(self, **overrides):
        value = {"active": True, "controller_thread": "01a1ce98-6aa1-7021-b9cd-99805a07b2b2",
                 "unit": "vist-mini-test.timer", "expires_epoch": 200, "max_wakes": 2, "wakes": 0,
                 "pending_id": None, "pending_since": None, "report_bed": str(self.bed),
                 "codex_binary": self.codex}
        value.update(overrides); self.lease_path.write_text(json.dumps(value)); return value

    def read(self): return json.loads(self.lease_path.read_text())

    def test_success_persists_one_pending_queue(self):
        self.lease(); self.assertEqual(0, heartbeat.run(self.lease_path, None, self.systemctl, 100))
        value = self.read(); self.assertEqual(value["last_result"], "queued"); self.assertEqual(value["wakes"], 1)
        self.assertTrue(value["pending_id"]); self.assertIn("queue queue --thread", self.calls.read_text())

    def test_pending_skips_second_queue(self):
        self.lease(pending_id="hb-retained", pending_since=99); self.assertEqual(0, heartbeat.run(self.lease_path, self.codex, self.systemctl, 100))
        self.assertEqual("pending", self.read()["last_result"]); self.assertFalse(self.calls.exists())

    def test_expiry_stops_only_valid_timer(self):
        self.lease(expires_epoch=100); self.assertEqual(0, heartbeat.run(self.lease_path, self.codex, self.systemctl, 100))
        self.assertFalse(self.read()["active"]); self.assertEqual("expired", self.read()["last_result"])
        self.assertIn("stop --user --no-block stop vist-mini-test.timer", self.calls.read_text())

    def test_queue_failure_keeps_uncertain_id_and_stops(self):
        self.lease(); old = os.environ.get("QUEUE_EXIT"); os.environ["QUEUE_EXIT"] = "7"
        try: self.assertEqual(0, heartbeat.run(self.lease_path, self.codex, self.systemctl, 100))
        finally:
            if old is None: os.environ.pop("QUEUE_EXIT", None)
            else: os.environ["QUEUE_EXIT"] = old
        value = self.read(); self.assertFalse(value["active"]); self.assertEqual("queue_exit_7", value["last_result"]); self.assertTrue(value["pending_id"])

    def test_queue_timeout_keeps_pending_id_deactivates_and_stops(self):
        self.lease()
        calls = []

        def run(command, **kwargs):
            calls.append(command)
            if command[0] == self.codex:
                raise subprocess.TimeoutExpired(command, kwargs["timeout"])
            return subprocess.CompletedProcess(command, 0)

        with mock.patch.object(heartbeat.subprocess, "run", side_effect=run):
            self.assertEqual(0, heartbeat.run(self.lease_path, self.codex, self.systemctl, 100))

        value = self.read()
        self.assertFalse(value["active"])
        self.assertEqual("queue_timeout", value["last_result"])
        self.assertTrue(value["pending_id"])
        self.assertIn([self.systemctl, "--user", "--no-block", "stop", "vist-mini-test.timer"], calls)

    def test_wake_budget_exhaustion_stops_without_queue(self):
        self.lease(wakes=2)
        calls = []

        def run(command, **kwargs):
            calls.append(command)
            return subprocess.CompletedProcess(command, 0)

        with mock.patch.object(heartbeat.subprocess, "run", side_effect=run):
            self.assertEqual(0, heartbeat.run(self.lease_path, self.codex, self.systemctl, 100))

        value = self.read()
        self.assertFalse(value["active"])
        self.assertEqual("wake_budget_exhausted", value["last_result"])
        self.assertEqual([[self.systemctl, "--user", "--no-block", "stop", "vist-mini-test.timer"]], calls)

    def test_invalid_unit_rejected_without_systemctl(self):
        self.lease(unit="other.timer")
        with self.assertRaisesRegex(ValueError, "unit"):
            heartbeat.run(self.lease_path, self.codex, self.systemctl, 100)
        self.assertFalse(self.calls.exists())


if __name__ == "__main__": unittest.main()
