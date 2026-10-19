import importlib.util
from pathlib import Path
import unittest
spec = importlib.util.spec_from_file_location('frames', Path(__file__).parents[1] / 'tools/analyze_frames.py')
frames = importlib.util.module_from_spec(spec)
spec.loader.exec_module(frames)

class FrameAnalysisTests(unittest.TestCase):
    def test_p99_exposes_hitch_despite_good_average(self):
        result = frames.summarize([16.] * 98 + [80., 150.], 1000/60)
        self.assertEqual(result['p99_ms'], 80)
        self.assertEqual(result['over_2x_budget'], 2)
        self.assertEqual(result['over_100ms'], 1)
    def test_native_30fps_is_not_a_hitch(self):
        result = frames.summarize([1000/30] * 300, 1000/30)
        self.assertEqual(result['over_2x_budget'], 0)
        self.assertAlmostEqual(result['interval_rate_hz'], 30)
    def test_invalid_trace_rejected(self):
        for samples in ([], [0], [-1], [float('nan')], [float('inf')]):
            with self.assertRaises(ValueError):
                frames.summarize(samples, 16.67)
    def test_invalid_budget_rejected(self):
        for budget in (0, -1, float('nan')):
            with self.assertRaises(ValueError):
                frames.summarize([16], budget)
if __name__ == '__main__':
    unittest.main()
