import pandas as pd


def spot(header, rows):
    """Return positions (0-based) of rows whose input values look wrong."""
    goals = ["MRE-", "ACC+", "PRED40+"]
    goal_cols = [c for c in header if c in goals]
    input_cols = [c for c in header if c not in goals and c != "?"]

    # Precompute best scores from the full dataset (step01 convention)
    bests = {}
    for g in goals:
        vals = []
        for r in rows:
            v = float(r[header.index(g)])
            if g.endswith("-"):
                vals.append(v)
            else:
                vals.append(-v)
        bests[g] = min(vals)

    # Score each row (lower is better)
    def score_row(row):
        s = 0.0
        for g in goals:
            v = float(row[header.index(g)])
            if g.endswith("-"):
                s += (v - bests[g])
            else:
                s += (-v - bests[g])
        return s

    # Score each row and find the worst ones
    scored = [(i, score_row(r)) for i, r in enumerate(rows)]
    scored.sort(key=lambda x: x[1], reverse=True)

    # Now check which rows have suspicious input values
    # A row is suspicious if its inputs are outliers compared to other rows with similar goals
    suspicious = []

    for i, s in scored:
        row = rows[i]
        # Check each input column for consistency
        for c in input_cols:
            col_idx = header.index(c)
            v = float(row[col_idx])

            # Get other rows with similar goal scores (within 10% of this row's score)
            similar_rows = [j for j, sj in scored if abs(sj - s) < abs(s) * 0.1 + 0.5]

            if len(similar_rows) >= 3:
                # Compute mean and std of this column among similar rows
                col_vals = []
                for j in similar_rows:
                    col_vals.append(float(rows[j][col_idx]))
                mean_val = sum(col_vals) / len(col_vals)
                std_val = (sum((x - mean_val) ** 2 for x in col_vals) / max(len(col_vals) - 1, 1)) ** 0.5

                # If this row's value is far from the group mean (more than 2 std), it's suspicious
                if std_val > 0 and abs(v - mean_val) > 2 * std_val:
                    suspicious.append(i)
                    break  # Only need one suspicious column per row

    return sorted(suspicious, reverse=True)


if __name__ == "__main__":
    df = pd.read_csv("Health-ClosedIssues0000.train.csv")
    header = list(df.columns)
    rows = [list(r) for r in df.values]

    suspicious = spot(header, rows)
    print(f"Suspicious rows: {suspicious}")
