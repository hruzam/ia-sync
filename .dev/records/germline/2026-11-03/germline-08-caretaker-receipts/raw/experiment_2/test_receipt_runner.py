#!/usr/bin/env python3
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import threading
import time
import unittest

MODULE = Path(__file__).with_name("receipt_runner.py")
spec = importlib.util.spec_from_file_location("receipt_runner", MODULE)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class ReceiptRunnerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name)
        self.operation = self.home / "peer-a.ask.operation.json"
        self.count = 0

    def tearDown(self):
        self.tmp.cleanup()

    def fake(self, argv):
        self.count += 1
        return __import__("subprocess").CompletedProcess(argv, 0, b"result", b"diagnostic")

    def test_completed_receipt_recovers_after_ignored_return(self):
        runner.run_operation(self.operation, ["fake", "ask"], self.home, executor=self.fake)
        self.assertEqual(runner.inspect(self.operation)["classification"], "completed-and-validated")

    def test_live_pending_is_running_until_blocked_fake_releases(self):
        started, release = threading.Event(), threading.Event()
        def blocked(argv):
            started.set()
            release.wait(2)
            return __import__("subprocess").CompletedProcess(argv, 0, b"ok", b"")
        thread = threading.Thread(target=runner.run_operation,
                                  args=(self.operation, ["fake", "ask"], self.home, blocked))
        thread.start()
        self.assertTrue(started.wait(1))
        self.assertEqual(runner.inspect(self.operation)["classification"], "running")
        release.set()
        thread.join(1)
        self.assertFalse(thread.is_alive())

    def test_dead_pending_is_unknown(self):
        self.operation.write_text(json.dumps({"status": "pending", "runner": {"pid": 999999, "start": "0"}}))
        self.assertEqual(runner.inspect(self.operation)["classification"], "unknown")

    def test_changed_output_is_unknown(self):
        runner.run_operation(self.operation, ["fake", "ask"], self.home, executor=self.fake)
        record = json.loads(self.operation.read_text())
        Path(record["outputs"]["stdout"]["path"]).write_text("altered")
        self.assertEqual(runner.inspect(self.operation)["classification"], "unknown")

    def test_nonzero_exit_is_failed_with_remote_outcome_unknown(self):
        failed = lambda argv: __import__("subprocess").CompletedProcess(argv, 7, b"", b"failure")
        runner.run_operation(self.operation, ["fake", "ask"], self.home, executor=failed)
        self.assertEqual(runner.inspect(self.operation)["classification"], "failed-with-remote-outcome-unknown")

    def test_malformed_receipt_is_unknown(self):
        self.operation.write_text("not-json")
        self.assertEqual(runner.inspect(self.operation)["classification"], "unknown")

    def test_wrong_json_shapes_are_unknown(self):
        cases = [None, [], {"status": "pending", "runner": []},
                 {"status": "pending", "runner": {"pid": "bad", "start": "1"}},
                 {"status": "completed", "exit": 0, "outputs": []},
                 {"status": "completed", "exit": 0, "outputs": {"stdout": {"path": []}}}]
        for value in cases:
            with self.subTest(value=value):
                self.operation.write_text(json.dumps(value))
                self.assertEqual(runner.inspect(self.operation)["classification"], "unknown")

    def test_nonobject_state_is_malformed(self):
        self.operation.write_text("null")
        self.assertEqual(runner.select_state(self.operation), {"state": "malformed"})

    def test_duplicate_refuses_without_second_fake_execution(self):
        runner.run_operation(self.operation, ["fake", "ask"], self.home, executor=self.fake)
        with self.assertRaises(RuntimeError):
            runner.run_operation(self.operation, ["fake", "ask"], self.home, executor=self.fake)
        self.assertEqual(self.count, 1)

    def test_fixed_open_is_pinned_and_low_effort(self):
        root = self.home / "experiment_2"
        args = runner.fixed_argv(root, "peer-a", "open")
        self.assertIn("gpt-6.1-sol", args)
        self.assertIn("effort=low", args)
        self.assertEqual(args[0], runner.SHIM)
        self.assertEqual(args[args.index("--cwd") + 1], str(root.parents[1]))


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ReceiptRunnerTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    report = {"command": "python3 test_receipt_runner.py", "testsRun": result.testsRun,
              "failures": len(result.failures), "errors": len(result.errors),
              "successful": result.wasSuccessful(),
              "checks": ["completed recovery", "live pending", "dead pending", "altered output", "nonzero exit", "malformed receipt", "duplicate refusal", "fixed low-effort argv"]}
    print(json.dumps(report, sort_keys=True))
    raise SystemExit(not result.wasSuccessful())
