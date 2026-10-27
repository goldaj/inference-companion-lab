"""Adversarial and happy-path checks for the offline study audit, no runtime or OS calls."""

from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from lab.scripts.audit_experiment import (
    InvalidStudy, audit_study, load_study, main,
)

A = "a" * 64
B = "b" * 64
C = "c" * 64
D = "d" * 64
E = "e" * 64


def study(*, origin="synthetic", status="candidate_not_frozen"):
    p = {
        "schema_version": 1, "experiment_id": "offline-example-only",
        "protocol_status": status, "origin": origin, "fidelity_contract": "E1",
        "model_sha256": A, "engine_sha256": B, "tokenizer_sha256": C,
        "prompt_suite_sha256": D, "trace_sha256": E,
        "minimum_gain_pct": 5.0, "min_blocks": 2,
        "minimum_improved_blocks": 2,
        "max_canary_p99_ms": 120.0, "max_canary_p99_regression_pct": 10.0,
        "max_observer_p99_regression_pct": 3.0,
        "fixed_window_seconds": 60.0, "seed": 42,
    }
    pre = []
    runs = []
    for num in range(2):
        blk = f"block-{num+1}"
        pre.extend([
            {"block_id": blk, "condition": "A0",
             "canary_p99_ms": 95.0, "observed_cpu_pct": 0.0},
            {"block_id": blk, "condition": "A1",
             "canary_p99_ms": 96.0, "observed_cpu_pct": 1.0},
        ])
        for name, toks, qos in [("A", 0, 100.0), ("B", 100, 104.0),
                                 ("C", 150, 160.0), ("D", 110, 105.0)]:
            runs.append({
                "block_id": blk, "scenario": name, "accepted_tokens": toks,
                "canary_p99_ms": qos, "e1_tokens_match_oracle": True,
                "stop_triggered": False, "duration_seconds": 60.0,
                "seed": 42, "model_sha256": A, "engine_sha256": B,
                "tokenizer_sha256": C, "prompt_suite_sha256": D,
                "trace_sha256": E,
            })
    return {"protocol": p, "observer_preflight": pre, "runs": runs}


def problems(payload):
    return audit_study(payload)["problems"]


class AuditExperimentTests(unittest.TestCase):
    def test_synthetic_candidate_never_proves_success(self):
        r = audit_study(study())
        self.assertEqual("NOT_ADMISSIBLE", r["decision"])
        self.assertEqual(2, r["paired_blocks"])
        self.assertAlmostEqual(10.0, r["pooled_gain_pct"])
        self.assertEqual(["PROTOCOL_NOT_PREREGISTERED",
                          "SYNTHETIC_NOT_EMPIRICAL_EVIDENCE"], r["problems"])
        self.assertIn("NOT a PASS", r["limitations"][3])

    def test_even_self_declared_measurements_only_reach_review_required(self):
        r = audit_study(study(origin="externally_measured", status="pre_registered"))
        self.assertEqual("REVIEW_REQUIRED", r["decision"])
        self.assertEqual([], r["problems"])

    def test_c_stress_arm_qos_violation_not_hidden_or_misapplied(self):
        r = audit_study(study(origin="externally_measured", status="pre_registered"))
        self.assertTrue(all(x["c_violates_absolute_qos"] for x in r["per_block"]))
        self.assertNotIn("QOS_BREACH", str(r["problems"]))

    def test_missing_scenario_never_counts_as_complete_block(self):
        p = study()
        p["runs"] = [x for x in p["runs"]
                     if not (x["block_id"] == "block-2" and x["scenario"] == "B")]
        self.assertIn("TOO_FEW_COMPLETE_ABCD_BLOCKS", problems(p))
        self.assertIn("INCOMPLETE_ABCD_BLOCK:block-2", problems(p))

    def test_duplicate_scenario_and_duplicate_preflight_block_rejected(self):
        for target in ("runs", "observer_preflight"):
            p = study()
            p[target].append(copy.deepcopy(p[target][0]))
            with self.assertRaisesRegex(InvalidStudy, "duplicate"):
                audit_study(p)

    def test_runtime_identities_and_window_are_checked_per_arm(self):
        p = study()
        p["runs"][3]["model_sha256"] = D
        p["runs"][4]["duration_seconds"] = 59
        p["runs"][5]["seed"] = 1337
        ps = problems(p)
        self.assertIn("INCONSISTENT_PROVENANCE:block-1/D/model_sha256", ps)
        self.assertIn("UNEQUAL_WINDOW:block-2/A", ps)
        self.assertIn("MISMATCHED_SEED:block-2/B", ps)

    def test_fidelity_and_stop_conditions(self):
        p = study()
        p["runs"][7]["e1_tokens_match_oracle"] = False
        p["runs"][3]["stop_triggered"] = True
        ps = problems(p)
        self.assertIn("FIDELITY_E1_NOT_CONFIRMED:block-2", ps)
        self.assertIn("STOP_TRIGGERED_IN_REFERENCE_OR_CANDIDATE:block-1", ps)

    def test_qos_interference_and_paired_gain_failure(self):
        p = study()
        p["observer_preflight"][1]["canary_p99_ms"] = 105
        p["runs"][3]["canary_p99_ms"] = 125
        p["runs"][7]["accepted_tokens"] = 90
        ps = problems(p)
        self.assertIn("OBSERVER_SELF_INTERFERENCE:block-1", ps)
        self.assertIn("QOS_BREACH:block-1/D", ps)
        self.assertIn("TOO_FEW_BLOCKS_WITH_IMPROVEMENT", ps)
        self.assertIn("MINIMUM_PAIRED_GAIN_NOT_MET", ps)

    def test_boolean_acceptance_does_not_coerce_numeric_zeros(self):
        p = study()
        p["runs"][0]["accepted_tokens"] = False
        with self.assertRaises(InvalidStudy):
            audit_study(p)
        p = study()
        p["protocol"]["max_canary_p99_ms"] = True
        with self.assertRaises(InvalidStudy):
            audit_study(p)

    def test_unexpected_fields_are_rejected_to_avoid_silent_data_acceptance(self):
        p = study()
        p["runs"][0]["prompt_text"] = "personal"
        with self.assertRaises(InvalidStudy):
            audit_study(p)

    def test_invalid_hash_or_missing_evidence_fails_closed(self):
        p = study()
        p["runs"][3]["trace_sha256"] = "NOT-A-HASH"
        with self.assertRaises(InvalidStudy):
            audit_study(p)
        p = study()
        p["observer_preflight"] = []
        self.assertIn("OBSERVER_PREFLIGHT_MISSING", problems(p))

    def test_input_json_rejects_duplicate_keys_and_nan(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "data.json"
            path.write_text('{"schema_version":1,"schema_version":2}', encoding="utf-8")
            with self.assertRaisesRegex(InvalidStudy, "duplicate JSON"):
                load_study(path)
            path.write_text('{"x": NaN}', encoding="utf-8")
            with self.assertRaisesRegex(InvalidStudy, "non-finite"):
                load_study(path)

    def test_cli_outputs_json_and_nonzero_for_synthetic(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "synthetic.json"
            path.write_text(json.dumps(study()), encoding="utf-8")
            self.assertEqual(1, main([str(path)]))
            self.assertEqual(2, main([str(Path(folder) / "missing.json")]))

    def test_manifest_constraints_cannot_be_silently_relaxed(self):
        p = study()
        p["protocol"]["minimum_improved_blocks"] = 3
        with self.assertRaises(InvalidStudy):
            audit_study(p)
        p = study()
        p["protocol"]["min_blocks"] = 1
        with self.assertRaises(InvalidStudy):
            audit_study(p)


if __name__ == "__main__":
    unittest.main()
