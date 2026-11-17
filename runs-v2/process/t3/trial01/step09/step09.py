import pandas as pd
import numpy as np


def spot(header, rows):
    goal_cols = [h for h in header if h.endswith('-')]
    input_cols = [h for h in header if not h.endswith('-')]

    df = pd.DataFrame(rows, columns=header)
    for col in goal_cols:
        df[col] = df[col].replace('?', np.nan).astype(float)

    suspicious = []

    for i in range(len(df)):
        row_score = 0.0

        for col in input_cols:
            val = df.iloc[i][col]

            if pd.isna(val):
                continue

            try:
                v = float(val)
                is_numeric = True
            except (ValueError, TypeError):
                is_numeric = False

            if is_numeric:
                vals = df[col].dropna()
                if len(vals) > 0:
                    mean = vals.mean()
                    std = vals.std()
                    if std == 0:
                        z = 0.0
                    else:
                        z = (v - mean) / std

                    if abs(z) > 3.0:
                        row_score += abs(z) * 2
            elif isinstance(val, str):
                vals = df[col].dropna()
                if len(vals) > 0:
                    known_vals = set(str(v).strip() for v in vals.values if pd.notna(v))
                    if val not in known_vals and '?' not in str(val):
                        row_score += 5.0

        if row_score > 0:
            suspicious.append((row_score, i))

    suspicious.sort(key=lambda x: -x[0])

    return [idx for _, idx in suspicious]


if __name__ == "__main__":
    df = pd.read_csv('pom3a.train.csv')
    header = list(df.columns)
    rows = [list(row) for row in df.values]

    result = spot(header, rows)
    print(f"Suspected mistyped/made-up records: {result}")
