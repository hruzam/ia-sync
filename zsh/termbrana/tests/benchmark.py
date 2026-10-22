#!/usr/bin/env python3
"""Phase 0 evidence tooling; fixed office budgets, no retuning or runtime integration."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import statistics
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_composer import frame


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--family", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--fixed", type=Path, required=True)
    args = parser.parse_args()
    rules = json.loads(args.fixed.read_text())
    assert rules["fixed_before_measurements"] and rules["samples_per_input"] == 30
    assert rules["budgets_ms"] == {"four_corpus_bodies":100, "1_MiB":500, "4_MiB":2000}
    assert rules["four_MiB_median_over_one_MiB_median_max"] == 5
    fixtures = args.evidence / "fixtures"
    # All generation occurs before starting any clock.
    for size in (1, 4):
        body = b"x" * (size*1024*1024-1) + b"\n"
        (fixtures / ("%d-MiB.md" % size)).write_bytes(frame(body))
    inputs = [("four_corpus_bodies", fixtures/"corpus.mixed.md", 38799),
              ("1_MiB", fixtures/"1-MiB.md", 1024*1024),
              ("4_MiB", fixtures/"4-MiB.md", 4*1024*1024)]
    report = dict(host=platform.node(), platform=platform.platform(), python=sys.version,
                  fixed_criteria_sha256=hashlib.sha256(args.fixed.read_bytes()).hexdigest(),
                  samples_per_input=30, p95_definition="29th sorted of 30", inputs=[])
    for label, path, body_size in inputs:
        raw = path.read_bytes()
        command = ["zsh", "-f", "-c", 'source "$1/base.zsh"; _tbc_check "$2"',
                   "tbc-benchmark", str(args.family.resolve()), str(path.resolve())]
        samples = []
        for _ in range(30):
            start = time.perf_counter_ns()
            result = subprocess.run(command, capture_output=True)
            elapsed = (time.perf_counter_ns()-start)/1_000_000
            assert (result.returncode, result.stdout, result.stderr) == (0,b"",b""), (label,result.returncode,result.stderr)
            samples.append(elapsed)
        median = statistics.median(samples)
        p95 = sorted(samples)[28]
        report["inputs"].append(dict(label=label, command=command, body_bytes=body_size,
                                     serialized_bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(),
                                     samples_ms=samples, median_ms=median, p95_ms=p95,
                                     budget_ms=rules["budgets_ms"][label], pass_p95=p95<=rules["budgets_ms"][label]))
    ratio = report["inputs"][2]["median_ms"]/report["inputs"][1]["median_ms"]
    report.update(four_to_one_median_ratio=ratio, pass_ratio=ratio<=5,
                  status="PASS" if all(i["pass_p95"] for i in report["inputs"]) and ratio<=5 else "FAIL")
    (args.evidence/"benchmark.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"], "p95_ms":{i["label"]:i["p95_ms"] for i in report["inputs"]},
                      "four_to_one_median_ratio":ratio}))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
