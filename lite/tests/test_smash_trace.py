import importlib.util
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).parents[1] / 'tools'))
import analyze_smash_trace as trace

class TraceTests(unittest.TestCase):
    def test_legacy(self):
        result = trace.analyze('16\n16\n100\n', 16.67, 0)
        self.assertEqual(result['p99_ms'], 100)
    def test_diagnostic(self):
        result = trace.analyze('interval_ms,shader_wait_calls,shader_wait_ms\n16,0,0\n100,2,80\n',16.67,0)
        self.assertEqual(result['diagnostics']['shader_wait']['completed_scopes'],2)
        self.assertEqual(result['diagnostics']['shader_wait']['total_scope_ms'],80)
        self.assertEqual(result['over_2x_budget'],1)
    def test_bad_diagnostic(self):
        with self.assertRaises(ValueError):
            trace.analyze('interval_ms,gpu_wait_calls,gpu_wait_ms\n16,1,nan\n',16.67,0)
