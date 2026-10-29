import json
import tempfile
import unittest
from pathlib import Path
from lab.scripts.observe_passive import ProbeConfig, measure, percentile, summarize, write_under_lab

class Clock:
    def __init__(self, delay_ns=0):
        self.now=0
        self.delay_ns=delay_ns
    def tick(self):
        return self.now
    def cpu(self):
        return self.now // 100
    def sleep(self,seconds):
        self.now+=round(seconds*1_000_000_000)+self.delay_ns

class ObserverTests(unittest.TestCase):
    def test_probe_configuration_is_bounded(self):
        for samples,interval in [(0,50),(241,50),(3,0),(3,3000)]:
            with self.assertRaises(ValueError):ProbeConfig(samples,interval).validate()

    def test_jitter_without_delay_is_zero(self):
        c=Clock()
        report=measure(ProbeConfig(5,100),clock_ns=c.tick,cpu_ns=c.cpu,sleeper=c.sleep)
        self.assertEqual(report["metrics"]["wake_delay_ms"]["p95"],0)
        self.assertEqual(report["metrics"]["elapsed_s"],0.5)
        self.assertEqual(len(report["samples"]),5)

    def test_observer_records_scheduling_delay(self):
        c=Clock(delay_ns=2_000_000)
        report=measure(ProbeConfig(5,50),clock_ns=c.tick,cpu_ns=c.cpu,sleeper=c.sleep)
        self.assertEqual(report["metrics"]["wake_delay_ms"]["p95"],2)
        self.assertGreater(report["metrics"]["observer_process_cpu_s"],0)
        self.assertFalse(report["inference_tokens_measured"])

    def test_percentiles_and_immutable_samples(self):
        values=[3.,1.,4.,2.,10.]
        before=values[:]
        self.assertEqual(percentile(values,.95),10)
        self.assertEqual(summarize(values)["p50"],3)
        self.assertEqual(values,before)

    def test_refuse_empty_and_nonfinite_measurements(self):
        with self.assertRaises(ValueError):summarize([])
        with self.assertRaises(ValueError):summarize([float("inf")])
        with self.assertRaises(ValueError):summarize([-1.0])

    def test_write_only_within_explicit_lab_root(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder).resolve()
            (root/"results").mkdir()
            dest=write_under_lab(root,"results/run.json",{"status":"synthetic"})
            self.assertEqual(json.loads(dest.read_text())["status"],"synthetic")
            with self.assertRaises(ValueError):write_under_lab(root,"results/run.json",{"status":"changed"})
            with self.assertRaises(ValueError):write_under_lab(root,"../outside.json",{})

    def test_no_directory_is_created_implicitly(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(ValueError):
                write_under_lab(Path(folder).resolve(),"missing/run.json",{})
            self.assertFalse((Path(folder)/"missing").exists())

    def test_cli_does_not_write_automatically(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            self.assertEqual(list(root.iterdir()),[])

if __name__=="__main__":unittest.main()
