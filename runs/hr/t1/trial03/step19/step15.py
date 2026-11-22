import csv

def blame(header, rows):
    """
    Identifies input columns that have the least correlation with the goal columns.
    We define 'bad' as columns that show no significant difference in distribution
    between the top 25% and bottom 25% of employees (ranked by composite goal score).
    Columns with the smallest difference are candidates for removal.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    input_indices = [i for i, name in enumerate(header) if not (name.endswith('+') or name.endswith('-'))]

    # Normalize goals to [0, 1] range to calculate a composite score
    def get_score(row):
        scores = []
        for i in goal_indices:
            col_data = [r[i] for r in rows]
            min_v, max_v = min(col_data), max(col_data)
            rng = max_v - min_v if max_v != min_v else 1
            norm = (row[i] - min_v) / rng
            if header[i].endswith('-'):
                norm = 1 - norm
            scores.append(norm)
        return sum(scores) / len(scores)

    # Rank rows by composite score
    scored_rows = sorted([(get_score(row), row) for row in rows])
    worst_rows = [r[1] for r in scored_rows[:len(rows) // 4]]
    best_rows = [r[1] for r in scored_rows[-len(rows) // 4:]]

    # Find inputs that differ LEAST between worst and best rows
    # These are the columns that have 'nothing to do' with the outcome
    diffs = []
    for i in input_indices:
        if isinstance(rows[0][i], (int, float)):
            worst_vals = [r[i] for r in worst_rows]
            best_vals = [r[i] for r in best_rows]
            avg_w = sum(worst_vals) / len(worst_vals)
            avg_b = sum(best_vals) / len(best_vals)
            # Normalize difference by range to make it comparable
            col_data = [r[i] for r in rows]
            rng = max(col_data) - min(col_data)
            rng = rng if rng != 0 else 1
            diffs.append((abs(avg_w - avg_b) / rng, header[i]))
        else:
            # For symbolic, check frequency difference (Jensen-Shannon-like heuristic)
            worst_vals = [r[i] for r in worst_rows]
            best_vals = [r[i] for r in best_rows]
            all_cats = set(worst_vals) | set(best_vals)
            score = 0
            for cat in all_cats:
                score += abs(worst_vals.count(cat)/len(worst_vals) - best_vals.count(cat)/len(best_vals))
            diffs.append((score, header[i]))

    # Sort by smallest difference
    diffs.sort(key=lambda x: x[0])
    return [d[1] for d in diffs[:5]]

def load_data(filename):
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
    return header, rows

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    header, rows = load_data(filename)
    factors = blame(header, rows)
    print("The following columns have the least impact on employee retention and could potentially be removed:")
    for f in factors:
        print(f"- {f}")
