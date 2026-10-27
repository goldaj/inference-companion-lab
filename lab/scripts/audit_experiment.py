"""Strict offline gate for a proposed inference-companion A0/A1 + A/B/C/D study.

No model execution, telemetry collection, OS actions, privilege elevation, or
network. This checks *declared* aggregate evidence for contradictions and
scientific omissions; it cannot authenticate measurements or certify QoS.
Only standard-library Python is required.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

MAX_INPUT_BYTES = 2_000_000
_SHA256 = re.compile(r"^[a-f0-9]{64}$")
_ID = re.compile(r"^[a-zA-Z0-9_.:-]{1,80}$")
_HASH_NAMES = ("model_sha256", "engine_sha256", "tokenizer_sha256",
               "prompt_suite_sha256", "trace_sha256")

PROTOCOL_KEYS = frozenset((
    "schema_version", "experiment_id", "protocol_status", "origin",
    "fidelity_contract", "model_sha256", "engine_sha256", "tokenizer_sha256",
    "prompt_suite_sha256", "trace_sha256", "minimum_gain_pct",
    "min_blocks", "max_canary_p99_ms", "max_canary_p99_regression_pct",
    "max_observer_p99_regression_pct", "minimum_improved_blocks",
    "fixed_window_seconds", "seed",
))
PRE_KEYS = frozenset(("block_id", "condition", "canary_p99_ms", "observed_cpu_pct"))
RUN_KEYS = frozenset(("block_id", "scenario", "accepted_tokens",
                      "canary_p99_ms", "e1_tokens_match_oracle",
                      "stop_triggered", "duration_seconds", "seed",
                      *_HASH_NAMES))
TOP_KEYS = frozenset(("protocol", "observer_preflight", "runs"))
SCENARIOS = frozenset(("A", "B", "C", "D"))


class InvalidStudy(ValueError):
    """Malformed or internally contradictory evidence, not an experiment failure."""


def _keys(obj: Any, expected: frozenset[str], context: str) -> dict[str, Any]:
    if not isinstance(obj, dict) or set(obj) != expected:
        raise InvalidStudy(f"{context}: expected exactly {sorted(expected)}; "
                           f"received {sorted(obj) if isinstance(obj, dict) else type(obj).__name__}")
    return obj


def _numeric(value: Any, where: str, *, low: float = 0, strictly: bool = False) -> float:
    if type(value) not in (float, int):
        raise InvalidStudy(f"{where}: finite numeric value required")
    try:
        finite = math.isfinite(value)
    except OverflowError:
        finite = False  # Python integer too large even to convert to float
    if not finite:
        raise InvalidStudy(f"{where}: finite numeric value required")
    if value < low or (strictly and value == low):
        raise InvalidStudy(f"{where}: outside admissible range")
    return float(value)


def _int(value: Any, where: str, *, low: int = 0) -> int:
    if type(value) is not int or value < low:
        raise InvalidStudy(f"{where}: integer >= {low} required")
    return value


def _hash(value: Any, where: str) -> str:
    if not isinstance(value, str) or not _SHA256.fullmatch(value):
        raise InvalidStudy(f"{where}: lowercase 64-digit sha256 string required")
    return value


def _id(value: Any, where: str) -> str:
    if not isinstance(value, str) or not _ID.fullmatch(value):
        raise InvalidStudy(f"{where}: restricted nonblank identifier required")
    return value


def _protocol(obj: Any) -> dict[str, Any]:
    p = _keys(obj, PROTOCOL_KEYS, "protocol")
    if _int(p["schema_version"], "schema_version") != 1:
        raise InvalidStudy("unsupported schema version")
    _id(p["experiment_id"], "experiment_id")
    if p["protocol_status"] not in ("candidate_not_frozen", "pre_registered"):
        raise InvalidStudy("protocol_status must be candidate_not_frozen or pre_registered")
    if p["origin"] not in ("synthetic", "externally_measured"):
        raise InvalidStudy("origin must be declared explicitly")
    if p["fidelity_contract"] != "E1":
        raise InvalidStudy("only a declared E1 protocol is handled")
    for name in _HASH_NAMES:
        _hash(p[name], f"protocol.{name}")
    _numeric(p["minimum_gain_pct"], "minimum_gain_pct", strictly=True)
    _numeric(p["max_canary_p99_ms"], "max_canary_p99_ms", strictly=True)
    _numeric(p["max_canary_p99_regression_pct"], "max_canary_p99_regression_pct")
    _numeric(p["max_observer_p99_regression_pct"], "max_observer_p99_regression_pct")
    _numeric(p["fixed_window_seconds"], "fixed_window_seconds", strictly=True)
    _int(p["seed"], "seed")
    _int(p["min_blocks"], "min_blocks", low=2)
    _int(p["minimum_improved_blocks"], "minimum_improved_blocks", low=1)
    if p["minimum_improved_blocks"] > p["min_blocks"]:
        raise InvalidStudy("minimum_improved_blocks cannot exceed min_blocks")
    return p


def _preflight(items: Any, p: dict[str, Any], problems: list[str]) -> dict[str, dict[str, dict]]:
    if not isinstance(items, list) or len(items) > 2000:
        raise InvalidStudy("observer_preflight must be a bounded list")
    grouped: dict[str, dict[str, dict]] = defaultdict(dict)
    for j, item in enumerate(items):
        i = _keys(item, PRE_KEYS, f"observer_preflight[{j}]")
        block = _id(i["block_id"], "preflight block")
        condition = i["condition"]
        if condition not in ("A0", "A1"):
            raise InvalidStudy("preflight condition must be A0 or A1")
        _numeric(i["canary_p99_ms"], "preflight.canary_p99_ms", strictly=True)
        _numeric(i["observed_cpu_pct"], "preflight.observed_cpu_pct")
        if i["observed_cpu_pct"] > 100:
            raise InvalidStudy("preflight CPU percentage cannot exceed 100")
        if condition in grouped[block]:
            raise InvalidStudy(f"duplicate observer record: {block}/{condition}")
        grouped[block][condition] = i
    if not grouped:
        problems.append("OBSERVER_PREFLIGHT_MISSING")
    for block, entries in sorted(grouped.items()):
        if set(entries) != {"A0", "A1"}:
            problems.append(f"OBSERVER_PAIR_INCOMPLETE:{block}")
            continue
        a0, a1 = entries["A0"], entries["A1"]
        inc = 100 * (a1["canary_p99_ms"] - a0["canary_p99_ms"]) / a0["canary_p99_ms"]
        if inc > p["max_observer_p99_regression_pct"]:
            problems.append(f"OBSERVER_SELF_INTERFERENCE:{block}")
    return grouped


def _runs(items: Any, p: dict[str, Any], problems: list[str]) -> dict[str, dict[str, dict]]:
    if not isinstance(items, list) or len(items) > 20_000:
        raise InvalidStudy("runs must be a bounded list")
    grouped: dict[str, dict[str, dict]] = defaultdict(dict)
    for j, item in enumerate(items):
        r = _keys(item, RUN_KEYS, f"runs[{j}]")
        block = _id(r["block_id"], "run block")
        scenario = r["scenario"]
        if scenario not in SCENARIOS:
            raise InvalidStudy("unknown scenario")
        if scenario in grouped[block]:
            raise InvalidStudy(f"duplicate run: {block}/{scenario}")
        _int(r["accepted_tokens"], "accepted_tokens")
        _numeric(r["canary_p99_ms"], "canary_p99_ms", strictly=True)
        _numeric(r["duration_seconds"], "duration_seconds", strictly=True)
        if abs(r["duration_seconds"] - p["fixed_window_seconds"]) > 1e-6:
            problems.append(f"UNEQUAL_WINDOW:{block}/{scenario}")
        if type(r["e1_tokens_match_oracle"]) is not bool or type(r["stop_triggered"]) is not bool:
            raise InvalidStudy("E1 and stop flags must be booleans")
        if _int(r["seed"], "run seed") != p["seed"]:
            problems.append(f"MISMATCHED_SEED:{block}/{scenario}")
        for name in _HASH_NAMES:
            _hash(r[name], f"run {name}")
            if r[name] != p[name]:
                problems.append(f"INCONSISTENT_PROVENANCE:{block}/{scenario}/{name}")
        grouped[block][scenario] = r
    if not grouped:
        problems.append("RUNS_MISSING")
    return grouped


def audit_study(study: Any) -> dict[str, Any]:
    """Deterministic structured diagnostics, never a proof of scientific success.

    Only one summary per scenario and block. Latency p99 is not reconstructed
    from raw observations: this tool checks reported values for consistency,
    and cannot infer uncertainty, temporal causality, or independent samples.
    """
    study = _keys(study, TOP_KEYS, "study")
    p = _protocol(study["protocol"])
    problems: list[str] = []
    pre = _preflight(study["observer_preflight"], p, problems)
    runs = _runs(study["runs"], p, problems)
    paired = sorted(b for b, group in runs.items() if set(group) == SCENARIOS)
    for b in sorted(runs):
        if set(runs[b]) != SCENARIOS:
            problems.append(f"INCOMPLETE_ABCD_BLOCK:{b}")
    if len(paired) < p["min_blocks"]:
        problems.append("TOO_FEW_COMPLETE_ABCD_BLOCKS")
    if len([b for b in pre if set(pre[b]) == {"A0", "A1"}]) < p["min_blocks"]:
        problems.append("TOO_FEW_COMPLETE_OBSERVER_BLOCKS")
    gains: list[float] = []
    paired_results = []
    for block in paired:
        a, b, c, d = (runs[block][k] for k in ("A", "B", "C", "D"))
        if a["accepted_tokens"] != 0:
            problems.append(f"A_HAS_INFERENCE_TOKENS:{block}")
        if b["accepted_tokens"] <= 0:
            problems.append(f"B_WITHOUT_TOKENS:{block}")
        if any(not item["e1_tokens_match_oracle"] for item in (b, c, d)):
            problems.append(f"FIDELITY_E1_NOT_CONFIRMED:{block}")
        if any(item["stop_triggered"] for item in (a, b, d)):
            problems.append(f"STOP_TRIGGERED_IN_REFERENCE_OR_CANDIDATE:{block}")
        # C is deliberately a stress/reference arm; report but do not treat
        # its QoS exceedance as grounds to disqualify B or D.
        for key, item in (("B", b), ("D", d)):
            regression = 100 * (item["canary_p99_ms"] - a["canary_p99_ms"]) / a["canary_p99_ms"]
            if (item["canary_p99_ms"] > p["max_canary_p99_ms"] or
                    regression > p["max_canary_p99_regression_pct"]):
                problems.append(f"QOS_BREACH:{block}/{key}")
        gain = None if b["accepted_tokens"] == 0 else (
            100 * (d["accepted_tokens"] / b["accepted_tokens"] - 1))
        if gain is not None:
            gains.append(gain)
        paired_results.append({
            "block_id": block,
            "b_accepted_tokens": b["accepted_tokens"],
            "d_accepted_tokens": d["accepted_tokens"],
            "gain_pct": gain,
            "c_violates_absolute_qos": c["canary_p99_ms"] > p["max_canary_p99_ms"],
        })
    if paired:
        b_tokens = sum(runs[k]["B"]["accepted_tokens"] for k in paired)
        d_tokens = sum(runs[k]["D"]["accepted_tokens"] for k in paired)
        total_gain = None if b_tokens <= 0 else 100 * (d_tokens / b_tokens - 1)
    else:
        total_gain = None
    if total_gain is None or total_gain < p["minimum_gain_pct"]:
        problems.append("MINIMUM_PAIRED_GAIN_NOT_MET")
    if sum(g >= p["minimum_gain_pct"] for g in gains) < p["minimum_improved_blocks"]:
        problems.append("TOO_FEW_BLOCKS_WITH_IMPROVEMENT")
    if p["protocol_status"] != "pre_registered":
        problems.append("PROTOCOL_NOT_PREREGISTERED")
    if p["origin"] != "externally_measured":
        problems.append("SYNTHETIC_NOT_EMPIRICAL_EVIDENCE")
    # 'externally_measured' is a self-declaration, not a cryptographic attestation.
    return {
        "schema_version": 1,
        "experiment_id": p["experiment_id"],
        "decision": "NOT_ADMISSIBLE" if problems else "REVIEW_REQUIRED",
        "problems": sorted(set(problems)),
        "paired_blocks": len(paired),
        "observer_pair_blocks": sum(set(v) == {"A0", "A1"} for v in pre.values()),
        "pooled_gain_pct": total_gain,
        "per_block": paired_results,
        "limitations": [
            "No raw traces, no authentic latency p99 reconstruction, no oracle execution.",
            "Hashes and E1 flags are self-declarations and cannot certify fidelity.",
            "No statistical significance estimate, no true independent-run verification.",
            "REVIEW_REQUIRED is NOT a PASS or a deployment authorization.",
        ],
    }


def _no_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    d: dict[str, Any] = {}
    for key, val in pairs:
        if key in d:
            raise InvalidStudy(f"duplicate JSON key: {key}")
        d[key] = val
    return d


def _reject_nonfinite(_: str) -> None:
    raise InvalidStudy("non-finite JSON constants forbidden")


def load_study(path: Path) -> Any:
    if path.stat().st_size > MAX_INPUT_BYTES:
        raise InvalidStudy("input exceeds offline bound")
    return json.loads(path.read_text(encoding="utf-8"),
                      object_pairs_hook=_no_duplicate_keys,
                      parse_constant=_reject_nonfinite)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only declared-evidence quality gate")
    parser.add_argument("study_json", type=Path, help="Synthetic or external aggregate JSON")
    args = parser.parse_args(argv)
    try:
        report = audit_study(load_study(args.study_json))
    except (InvalidStudy, OSError, UnicodeError, json.JSONDecodeError, RecursionError) as e:
        print(json.dumps({"decision": "INVALID_INPUT", "error": str(e)}, sort_keys=True))
        return 2
    print(json.dumps(report, sort_keys=True, indent=2, allow_nan=False))
    return 0 if report["decision"] == "REVIEW_REQUIRED" else 1


if __name__ == "__main__":
    sys.exit(main())
