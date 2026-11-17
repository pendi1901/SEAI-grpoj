import pandas as pd
import numpy as np


def spot(header, rows):
    goal_cols = [c for c in header if c.endswith('-')]
    input_cols = [c for c in header if not c.endswith('-')]

    n = len(rows)
    scores = np.zeros(n)
    for col in goal_cols:
        vals = np.array([float(r[header.index(col)]) for r in rows])
        sorted_idx = np.argsort(vals)
        ranks = np.zeros(n)
        ranks[sorted_idx] = np.arange(n, 0, -1) / n
        scores += ranks

    # Compute residuals: how far each row's goals deviate from the expected pattern.
    # For each goal column, fit a simple linear model on input columns and check residual.
    suspicious = []
    for col in goal_cols:
        vals = np.array([float(r[header.index(col)]) for r in rows])
        X = np.column_stack([np.array([float(r[header.index(c)]) for r in rows]) for c in input_cols])

        # Use median absolute deviation as a robust measure of fit.
        residuals = []
        for i in range(n):
            pred = 0.0
            for j, c in enumerate(input_cols):
                coef = np.median(vals) / n * (1.0 if True else 0.0)  # placeholder
            # Instead, use a simple approach: compare each row's goal value to the
            # expected value based on its input features using rank correlation residuals.
            pass

    # Better approach: for each row, compute how unusual its goal values are compared
    # to rows with similar input profiles. Use local outlier factor via z-score of goals
    # weighted by similarity in inputs.
    suspicious = []
    for i in range(n):
        row_inputs = [float(rows[i][header.index(c)]) for c in input_cols]
        row_goals = [float(rows[i][header.index(col)]) for col in goal_cols]

        # Find similar rows (cosine similarity on inputs)
        best_sim_score = float('inf')
        for j in range(n):
            if i == j:
                continue
            other_inputs = [float(rows[j][header.index(c)] - float(rows[i][header.index(c)]) for c in input_cols]
            dist = np.sqrt(sum(x * x for x in other_inputs))
            if dist < best_sim_score:
                best_sim_score = dist

        # If a row is very different from all others but has extreme goals, flag it.
        goal_mean = np.mean(row_goals)
        goal_std = np.std(row_goals) if n > 1 else 0.0
        z_goal = (goal_mean - np.mean([np.mean([float(rows[k][header.index(col)]) for col in goal_cols]) for k in range(n)])) / goal_std if goal_std > 0 else 0.0

    # Simpler and more robust: detect rows where any input column value is an outlier
    # compared to the rest of the data, using IQR method.
    suspicious = []
    for col in input_cols:
        vals = np.array([float(r[header.index(col)]) for r in rows])
        q1, q3 = np.percentile(vals, [25, 75])
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        outlier_mask = (vals < lower) | (vals > upper)
        for idx in np.where(outlier_mask)[0]:
            suspicious.append(int(idx))

    # Also check goal columns for impossible values (negative scores, etc.)
    for col in goal_cols:
        vals = [float(r[header.index(col)]) for r in rows]
        for i, v in enumerate(vals):
            if v < -1.0 or v > 2.0:
                suspicious.append(i)

    # Remove duplicates and sort by suspicion (most extreme first)
    suspicious = sorted(set(suspicious), key=lambda x: abs(float(rows[x]['Cost-']) + float(rows[x]['Idle-'])))

    return suspicious


if __name__ == "__main__":
    df = pd.read_csv("pom3a.train.csv")
    header = list(df.columns)
    rows = [list(r) for _, r in df.iterrows()]

    answer = spot(header, rows)
    print(f"Suspect {len(answer)} mistyped/made-up records:")
    for pos in answer:
        print(f"  Row {pos}: Cost-={df.iloc[pos]['Cost-']:.4f}, Idle-={df.iloc[pos]['Idle-']:.4f}")
