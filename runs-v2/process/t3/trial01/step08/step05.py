import pandas as pd
import numpy as np


def blame(header, rows):
    goal_cols = [h for h in header if h.endswith('-')]
    input_cols = [h for h in header if not h.endswith('-')]

    df = pd.DataFrame(rows, columns=header)
    for col in goal_cols:
        df[col] = df[col].replace('?', np.nan).astype(float)

    # Normalize each goal to z-scores (low is good for '-', high is good for '+')
    scores = {}
    for col in goal_cols:
        vals = df[col].dropna()
        if len(vals) == 0:
            continue
        mean = vals.mean()
        std = vals.std()
        if std == 0:
            z_scores = np.zeros(len(df))
        else:
            z_scores = (df[col] - mean) / std
        scores[col] = z_scores

    # Composite score: average across all goals
    avg_score = np.mean([scores[c] for c in scores], axis=1)

    # Identify worst rows (lowest composite score)
    n_worst = max(1, int(len(rows) * 0.1))
    worst_idx = np.argsort(avg_score)[:n_worst]
    worst_mask = np.zeros(len(df), dtype=bool)
    worst_mask[worst_idx] = True

    # For each input column, measure how well it predicts being in the worst set
    correlations = {}
    for col in input_cols:
        vals = df[col].values
        if vals.dtype.kind == 'O':  # symbolic / categorical
            encoded = np.zeros(len(df))
            for i in range(len(df)):
                v = vals[i]
                if pd.isna(v):
                    continue
                if isinstance(v, str) and '?' not in v:
                    encoded[i] = 1.0
            correlations[col] = np.corrcoef(encoded, avg_score)[0, 1]
        else:
            correlations[col] = np.corrcoef(vals, avg_score)[0, 1]

    # Sort by absolute correlation descending and return top input columns
    sorted_cols = sorted(correlations.keys(), key=lambda c: abs(correlations[c]), reverse=True)
    return sorted_cols[:5]


if __name__ == "__main__":
    df = pd.read_csv('pom3a.train.csv')
    header = list(df.columns)
    rows = [list(row) for row in df.values]
    result = blame(header, rows)
    print(f"Top {len(result)} input columns explaining worst setups: {result}")
