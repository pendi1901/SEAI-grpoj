import ezr
from step01 import remember


def fix(header, row, levers):
    """Return {column: new_value} that best improves a bad row."""
    tbl = ezr.Tbl(iter([header] + [row]))

    # Compute ydist of the original row (with goals as-is)
    orig_yd = ezr.ydist(tbl, row)

    # Try every combination of lever values; pick the combo with lowest ydist.
    # If combos explode (>10k), fall back to single-lever changes only.
    names = list(levers.keys())
    vals_list = [levers[n] for n in names]

    if all(isinstance(v, (list, tuple)) and len(v) <= 5 for v in vals_list):
        # Small enough: try all combos
        from itertools import product
        best_combo = None
        best_yd = orig_yd
        for combo in product(*vals_list):
            trial = list(row)
            for i, n in enumerate(names):
                trial[n] = combo[i]
            yd = ezr.ydist(tbl, trial)
            if yd < best_yd:
                best_yd = yd
                best_combo = combo

        return dict(zip(names, best_combo))
    else:
        # Too many combos; try each lever individually first.
        best_single = None
        best_yd = orig_yd
        for n in names:
            vlist = levers[n]
            if isinstance(vlist, (list, tuple)):
                for v in vlist:
                    trial = list(row)
                    trial[n] = v
                    yd = ezr.ydist(tbl, trial)
                    if yd < best_yd:
                        best_yd = yd
                        best_single = {n: v}
            else:  # numeric (low, high) — try midpoint and extremes
                lo, hi = vlist
                for v in [lo, hi]:
                    trial = list(row)
                    trial[n] = v
                    yd = ezr.ydist(tbl, trial)
                    if yd < best_yd:
                        best_yd = yd
                        best_single = {n: v}
        return best_single or {}


if __name__ == "__main__":
    import csv

    with open("WA_Fn-UseC_-HR-Employee-Attrition.train.csv", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [next(reader) for _ in range(1470)]

    # Find a bad row (high ydist — someone who left or is at risk)
    ys = [ezr.ydist(ezr.Tbl(iter([header] + [r])), r) for r in rows[:5]]
    # Use the first few to calibrate; pick worst among them
    tbl0 = ezr.Tbl(iter([header] + rows[:1]))

    # Just use remember's top indices to find a bad row from training
    bad_idx = remember(header, rows)[0] if remember(header, rows) else 0
    bad_row = rows[bad_idx]

    # Define reasonable lever ranges based on the data
    levers = {
        "businessTravel": ["Non-Travel", "Travel_Rarely"],
        "overTime": ["N", "Y"],
        "PercentSalaryHike": (0, 25),
        "trainingTimesLastYear": [0, 3],
        "stockOptionLevel": [0, 4],
    }

    fix_dict = fix(header, bad_row, levers)
    print(f"Bad row ydist: {ezr.ydist(tbl0, bad_row):.3f}")
    print("Recommended changes:")
    for col, val in fix_dict.items():
        print(f"  {col}: {val}")
