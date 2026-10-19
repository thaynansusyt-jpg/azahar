"""Summarize one numeric millisecond sample per line (nearest-rank p99)."""
import argparse
import json
import math
from pathlib import Path

def summarize(samples, budget_ms):
    if not math.isfinite(budget_ms) or budget_ms <= 0:
        raise ValueError('budget must be positive and finite')
    if not samples or any(not math.isfinite(x) or x <= 0 for x in samples):
        raise ValueError('need positive, finite frame samples')
    ordered = sorted(samples)
    mean = math.fsum(samples) / len(samples)
    return {
        'samples': len(samples), 'mean_ms': mean,
        'p99_ms': ordered[math.ceil(len(ordered) * .99) - 1],
        'max_ms': ordered[-1],
        'over_2x_budget': sum(x > 2 * budget_ms for x in samples),
        'over_50ms': sum(x > 50 for x in samples),
        'over_100ms': sum(x > 100 for x in samples),
        'sample_duration_seconds': math.fsum(samples) / 1000,
        'interval_rate_hz': 1000 / mean
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv', type=Path)
    parser.add_argument('--budget-ms', type=float, required=True)
    parser.add_argument('--skip', type=int, default=5)
    args = parser.parse_args()
    if args.skip < 0:
        parser.error('--skip must be nonnegative')
    values = [float(line) for line in args.csv.read_text().splitlines() if line.strip()]
    result = summarize(values[args.skip:], args.budget_ms)
    result['source'] = str(args.csv)
    result['interpretation'] = 'Interval rate is FPS only for a game-submission interval trace; CPU-processing CSV is not presentation FPS.'
    print(json.dumps(result, indent=2))
if __name__ == '__main__':
    main()
