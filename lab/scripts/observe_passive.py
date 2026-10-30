"""L0 scheduling canary: zero model access, zero privilege, no host configuration changes.

This is an *observer overhead/baseline probe*, not an inference performance benchmark.
Default behavior prints JSON only and creates no files.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import platform
import statistics
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class ProbeConfig:
    samples: int = 20
    interval_ms: int = 50

    def validate(self) -> None:
        if type(self.samples) is not int or not 2 <= self.samples <= 240:
            raise ValueError("samples must be between 2 and 240")
        if type(self.interval_ms) is not int or not 10 <= self.interval_ms <= 2000:
            raise ValueError("interval_ms must be between 10 and 2000")


def percentile(samples: list[float], fraction: float) -> float:
    if not samples or not 0 <= fraction <= 1:
        raise ValueError("Invalid samples or percentile")
    ascending = sorted(samples)
    pos = math.ceil(fraction * len(ascending)) - 1
    return round(ascending[max(0, pos)], 4)


def summarize(values: list[float]) -> dict[str, float | int]:
    if not values or any(not math.isfinite(x) or x < 0 for x in values):
        raise ValueError("Expected nonempty finite nonnegative measurements")
    return {
        "count": len(values),
        "mean": round(statistics.fmean(values), 4),
        "p50": percentile(values, .5),
        "p95": percentile(values, .95),
        "p99": percentile(values, .99),
        "max": round(max(values), 4),
    }


def measure(
    config: ProbeConfig,
    *,
    clock_ns=time.perf_counter_ns,
    cpu_ns=time.process_time_ns,
    sleeper=time.sleep,
) -> dict:
    """A bounded sleep-wakeup latency experiment with test-injectable clocks."""
    config.validate()
    interval_ns = config.interval_ms * 1_000_000
    started = clock_ns()
    cpu_start = cpu_ns()
    entries = []
    for i in range(1, config.samples + 1):
        deadline = started + i * interval_ns
        now = clock_ns()
        if deadline > now:
            sleeper((deadline-now)/1_000_000_000)
        wake = clock_ns()
        delay_ms = max(0, (wake-deadline)/1_000_000)
        entries.append({
            "sample": i,
            "scheduled_ms": round(i*config.interval_ms, 4),
            "wake_delay_ms": round(delay_ms, 4),
        })
    end = clock_ns()
    cpu_end = cpu_ns()
    elapsed_s = (end-started)/1_000_000_000
    cpu_s = max(0, (cpu_end-cpu_start)/1_000_000_000)
    if elapsed_s <= 0:
        raise ValueError("Clock did not advance")
    delays = [e["wake_delay_ms"] for e in entries]
    return {
        "schema_version": 1,
        "kind": "L0_scheduler_canary",
        "model_loaded": False,
        "inference_tokens_measured": False,
        "configuration": {"samples": config.samples, "interval_ms": config.interval_ms},
        "metrics": {
            "wake_delay_ms": summarize(delays),
            "elapsed_s": round(elapsed_s, 4),
            "observer_process_cpu_s": round(cpu_s, 4),
            "observer_process_cpu_over_wall_percent": round(100*cpu_s/elapsed_s, 4),
        },
        "samples": entries,
        "limitations": [
            "No inference, no token accuracy, no GPU/VRAM telemetry",
            "Sleep scheduling jitter is not user-interface responsiveness",
            "Process CPU time is not whole-system utilization",
            "A production baseline requires repeated thermal and user-workload trials",
        ],
    }


def write_under_lab(root: Path, relative: str, data: dict) -> Path:
    if not root.is_absolute() or not root.is_dir():
        raise ValueError("lab-root must be an existing absolute directory")
    if not relative or Path(relative).is_absolute():
        raise ValueError("Report path must be relative")
    canonical = root.resolve()
    destination = (canonical / relative).resolve()
    if not destination.is_relative_to(canonical) or destination == canonical:
        raise ValueError("Report escapes the laboratory root")
    if destination.exists():
        raise ValueError("Report already exists; originals are never overwritten")
    if not destination.parent.is_dir():
        raise ValueError("Create a dedicated results directory before running")
    # x mode prevents overwrites, including a race with another process.
    with destination.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return destination


def cli(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Passive non-privileged L0 CPU scheduler canary")
    parser.add_argument("--samples", type=int, default=20)
    parser.add_argument("--interval-ms", type=int, default=50)
    parser.add_argument("--report", help="Optional relative output path within an existing lab root")
    parser.add_argument("--lab-root", type=Path, help="Existing absolute laboratory root, required with --report")
    args = parser.parse_args(argv)
    try:
        config = ProbeConfig(args.samples, args.interval_ms)
        config.validate()
        if args.report and args.lab_root is None:
            raise ValueError("Explicit --lab-root is required for disk export")
        if args.report and (not args.lab_root.is_absolute() or
                            not (args.lab_root / Path(args.report).parent).is_dir()):
            raise ValueError("Output directory must already exist inside lab root")
        report = measure(config)
        report["run_started_utc"] = datetime.now(timezone.utc).isoformat()
        report["host"] = {
            "system": platform.system(),
            "release": platform.release(),
            "architecture": platform.machine(),
            "logical_cpus": os.cpu_count(),
        }
        if args.report:
            destination = write_under_lab(args.lab_root, args.report, report)
            print("Saved L0 report: " + str(destination), file=sys.stderr)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, TypeError) as exc:
        print("L0 observer refused: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(cli())
