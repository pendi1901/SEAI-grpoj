import pandas as pd
from step01 import remember


def flow(header, row, seen):
    """Return True when we have a good enough setup to ship."""
    goal_cols = [c for c in header if c.endswith('-') or c.endswith('+')]

    # Track best values and worst scores across all rows seen so far (including current)
    min_vals = {}
    max_vals = {}
    for col in goal_cols:
        vals = []
        for r in seen + [row]:
            cell = r[header.index(col)]
            if cell == "?" or (isinstance(cell, float) and pd.isna(cell)):
                continue
            v = float(cell)
            vals.append(v)

        if '-' in col:
            min_vals[col] = min(vals) if vals else 0.0
        else:
            max_vals[col] = max(vals) if vals else 0.0

    # Score each row seen so far against the best values found across all rows
    scores = []
    for r in seen + [row]:
        s = 0.0
        valid = True
        for col in goal_cols:
            cell = r[header.index(col)]
            if cell == "?" or (isinstance(cell, float) and pd.isna(cell)):
                continue
            v = float(cell)
            if '-' in col:
                s += abs(v - min_vals[col])
            else:
                s += abs(v - max_vals[col])
        scores.append(s)

    # Check if the current row is among the best (top 5%) of all rows seen so far
    n = len(seen + [row])
    k = max(1, int(n * 0.05))
    sorted_indices = np.argsort(scores)[:k]
    
    # Return True if current row is in top-k
    return (len(seen + [row]) - 1) in sorted_indices.tolist()


if __name__ == "__main__":
    df = pd.read_csv("Health-ClosedIssues0000.train.csv")
    header = list(df.columns)
    rows = []
    for _, row in df.iterrows():
        cells = []
        for col in header:
            val = row[col]
            if isinstance(val, float):
                cells.append(float(val))
            else:
                cells.append(str(val))
        rows.append(cells)

    print(f"Loaded {len(rows)} setups from CSV.")
    
    # Simulate streaming: feed rows one at a time to flow() and stop when True
    import numpy as np
    
    for i, row in enumerate(rows):
        if flow(header, row, rows[:i]):
            print(f"Shipped setup {i} (MRE={row[header.index('MRE-')]:.4f}, ACC={row[header.index('ACC+')]:.4f})")
            break
    else:
        # If we never returned True, ship the last row as fallback
        print(f"No early stop triggered; shipping last setup {len(rows)-1}")
