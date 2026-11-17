import pandas as pd
import numpy as np


def remember(header, rows):
    goal_cols = [h for h in header if h.endswith('-')]

    df = pd.DataFrame(rows, columns=header)
    for col in goal_cols:
        df[col] = df[col].replace('?', np.nan).astype(float)

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

    if len(scores) > 0:
        avg_score = np.mean([scores[c] for c in scores], axis=1)
    else:
        return []

    n_rows = len(rows)
    max_return = max(1, int(n_rows * 0.05))
    top_indices = np.argsort(avg_score)[:max_return]

    return sorted(top_indices.tolist())


if __name__ == "__main__":
    df = pd.read_csv('pom3a.train.csv')
    header = list(df.columns)
    rows = [list(row) for row in df.values]
    result = remember(header, rows)
    print(f"Top {len(result)} out of {len(rows)} setups:")
    for idx in result:
        print(
            f"  Row {idx}: Cost-={df.iloc[idx]['Cost-']:.4f}, "
            f"Score-={df.iloc[idx]['Score-']:.4f}, Idle-={df.iloc[idx]['Idle-']:.4f}"
        )
