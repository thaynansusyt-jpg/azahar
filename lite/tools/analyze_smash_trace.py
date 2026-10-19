"""Analyze 0.1 numeric game-interval CSV or 0.2 diagnostic CSV (host Python 3)."""
import argparse
import csv
import io
import json
import math
from pathlib import Path
from analyze_frames import summarize


def analyze(text, budget_ms, skip=5):
    if skip < 0:
        raise ValueError('skip must be nonnegative')
    if text.lstrip().startswith('interval_ms,'):
        rows = list(csv.DictReader(io.StringIO(text)))[skip:]
        result = summarize([float(row['interval_ms']) for row in rows], budget_ms)
        categories = {}
        for key in (rows[0] if rows else {}):
            if not key.endswith('_calls'):
                continue
            name = key[:-6]
            calls = [int(row[key]) for row in rows]
            times = [float(row[name + '_ms']) for row in rows]
            if any(x < 0 for x in calls) or any(not math.isfinite(x) or x < 0 for x in times):
                raise ValueError('invalid diagnostic counter')
            categories[name] = {'completed_scopes': sum(calls), 'total_scope_ms': math.fsum(times),
                                'largest_frame_bucket_ms': max(times)}
        result['diagnostics'] = categories
    else:
        result = summarize([float(x) for x in text.splitlines() if x.strip()][skip:], budget_ms)
    result['limits'] = ('GSP game-submission intervals, not physical display presentation. '
                        'Scope totals can overlap and run on parallel threads; do not add them or '
                        'infer causality. Work is attributed when a scope completes. '
                        'A pipeline_build includes shader waits and cache-control probes. '
                        'gl_shader_path includes cache hits, compilation and cache writes. '
                        'storage covers IOFile paths, not all Android/provider I/O. '
                        'Emulation speed, RAM and temperature require separate device observations.')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv', type=Path)
    parser.add_argument('--budget-ms', type=float, required=True)
    parser.add_argument('--skip', type=int, default=5)
    parser.add_argument('--label', default='unlabelled')
    args = parser.parse_args()
    try:
        result = analyze(args.csv.read_text(), args.budget_ms, args.skip)
    except (ValueError, KeyError) as error:
        parser.error(str(error))
    result.update(source=str(args.csv), label=args.label)
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
