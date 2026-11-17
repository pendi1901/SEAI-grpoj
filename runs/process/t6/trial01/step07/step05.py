import ezr
from math import sqrt


def blame(header, rows):
    """Return input column names that best explain why the worst rows are bad."""
    # Identify goal columns (end with '-' or '+')
    goals = [(i, h.endswith('-')) for i, h in enumerate(header)
              if h.endswith('-') or h.endswith('+')]

    # Build table and compute ydist for each row
    tbl = ezr.Tbl(rows)
    ydists = [ezr.ydist(tbl, r) for r in rows]

    # Sort by ydist descending; worst rows have highest ydist
    worst_idx = sorted(range(len(ydists)), key=lambda i: ydists[i], reverse=True)
    worst_rows = [rows[i] for i in worst_idx[:min(10, len(rows))]]

    # Identify input columns (not goals)
    goal_indices = {gi for gi, _ in goals}
    inputs = [(i, h) for i, h in enumerate(header) if i not in goal_indices]

    # For each input column, compute Pearson correlation with ydist
    n = len(rows)
    mean_yd = sum(ydists) / max(1, n)
    sd_yd = sqrt(sum((y - mean_yd) ** 2 for y in ydists))

    results = []
    for ii, name in inputs:
        col_vals = [r[ii] if isinstance(r[ii], (int, float)) else 0.0 for r in rows]
        mean_x = sum(col_vals) / max(1, n)
        sd_x = sqrt(sum((v - mean_x) ** 2 for v in col_vals))

        if sd_x < 1e-32 or sd_yd < 1e-32:
            corr = 0.0
        else:
            num = sum((col_vals[i] - mean_x) * (ydists[i] - mean_yd) for i in range(n))
            corr = num / (sd_x * sd_yd)

        results.append((abs(corr), name, ii))

    # Sort by absolute correlation descending; return top inputs
    results.sort(key=lambda x: -x[0])
    return [name for _, name, _ in results]


if __name__ == "__main__":
    import os
    path = os.path.join(os.path.dirname(__file__) or ".", "pom3a.train.csv")
    with open(path, encoding="utf-8-sig") as f:
        lines = [l.strip() for l in f if l.strip()]
    header = lines[0].split(",")

    rows = []
    for line in lines[1:]:
        cells = line.split(",")
        row = []
        for c in cells:
            s = c.strip()
            try: row.append(float(s))
            except ValueError:
                if s.lower() == "true":  row.append(True)
                elif s.lower() == "false": row.append(False)
                else:                   row.append(s)
        rows.append(row)

    b = blame(header, rows)
    print(f"Blame for worst setups (high Idle-): {b}")
