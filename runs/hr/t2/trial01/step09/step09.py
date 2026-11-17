import csv


def spot(header, rows):
    """Find rows with suspicious hand-typed input values."""
    goal_cols = [c for c in header if c.endswith('+')]
    feature_cols = [c for c in header if not c.endswith('+') and c != 'attrition']

    n = len(rows)
    p = len(feature_cols)

    # For each numeric column, compute statistics from all OTHER rows (leave-one-out)
    suspicious_scores = []

    for i in range(n):
        row = rows[i]
        score = 0.0
        is_suspicious = False

        for j in range(p):
            col_name = feature_cols[j]
            try:
                val = float(row[header.index(col_name)])
            except ValueError:
                # Symbolic column - check if value matches expected categories
                col_idx = header.index(col_name)
                current_val = row[col_idx]

                # Count how many other rows have this same value
                count = 0
                for k in range(n):
                    if k != i:
                        if rows[k][col_idx] == current_val:
                            count += 1

                # If no other row has this value, it's suspicious
                if count == 0:
                    is_suspicious = True
                    score -= 2.0
                else:
                    score += count * 0.1
                continue

            # Numeric column: check against other rows' statistics
            others = []
            for k in range(n):
                if k != i:
                    try:
                        v = float(rows[k][header.index(col_name)])
                        others.append(v)
                    except ValueError:
                        pass

            if len(others) < 2:
                continue

            mean_o = sum(others) / len(others)
            var_o = sum((v - mean_o) ** 2 for v in others) / (len(others) - 1)
            std_o = var_o ** 0.5

            if std_o > 1e-10:
                z = abs(val - mean_o) / std_o
                score -= z * 0.5
                if z > 2.0:
                    is_suspicious = True

        suspicious_scores.append((score, i))

    # Sort by suspicion (most negative first)
    suspicious_scores.sort()

    return [int(pos) for _, pos in suspicious_scores[:10]]


if __name__ == "__main__":
    with open("WA_Fn-UseC_-HR-Employee-Attrition.train.csv", "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    positions = spot(header, rows)

    print(f"Suspicious row positions (most suspicious first): {positions}")
