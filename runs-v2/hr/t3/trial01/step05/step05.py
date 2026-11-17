def blame(header, rows):
    """Returns a list of strings - names of input columns that best explain why the worst rows are bad."""

    goal_cols = [col for col in header if col.endswith('+')]
    input_cols = [col for col in header if not col.endswith('+') and not col.endswith('-')]

    # Compute scores: sum of normalized + goals (higher is better)
    max_vals = {}
    for col in goal_cols:
        vals = []
        for row in rows:
            val = float(row[header.index(col)]) if isinstance(row[header.index(col)], (int, float)) else 0.0
            vals.append(val)
        max_vals[col] = max(vals) if vals else 1.0

    scores = []
    for row in rows:
        total = 0.0
        for col in goal_cols:
            val = float(row[header.index(col)]) if isinstance(row[header.index(col)], (int, float)) else 0.0
            total += val / max_vals[col]
        scores.append(total)

    # Find worst rows (lowest scores - shortest stays)
    n_worst = max(1, int(len(rows) * 0.05))
    worst_indices = sorted(range(len(scores)), key=lambda i: scores[i])[:n_worst]

    # For each input column, compute correlation with being in the worst group
    import numpy as np

    best_features = []
    for col in input_cols:
        idx = header.index(col)
        vals = [float(row[idx]) if isinstance(row[idx], (int, float)) else 0.0 for row in rows]
        arr_x = np.array(vals)
        arr_y = np.array(scores)
        corr = np.corrcoef(arr_x, arr_y)[0, 1]

        best_features.append((col, corr))

    # Sort by absolute correlation (strongest predictors first)
    best_features.sort(key=lambda x: abs(x[1]), reverse=True)

    return [f"{col} ({abs(corr):.3f})" for col, corr in best_features[:5]]


if __name__ == "__main__":
    import pandas as pd

    df = pd.read_csv('WA_Fn-UseC_-HR-Employee-Attrition.train.csv')
    header = list(df.columns)

    rows = []
    for _, row in df.iterrows():
        r = []
        for col, val in zip(header, row):
            if pd.isna(val):
                r.append(float('nan'))
            elif isinstance(val, (int, float)):
                r.append(float(val))
            else:
                r.append(str(val))
        rows.append(r)

    result = blame(header, rows)
    print(f"Factors explaining short stays:")
    for factor in result:
        print(f"  {factor}")
