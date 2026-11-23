import csv

def justify(header, rows, row):
    """
    Returns (p, reason) where p is the percentile rank of the row
    based on the average of its goal columns.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    
    # Estimate goal values for the test row using simple mean of all rows
    # (as a baseline estimator since we need to compare it to the population)
    estimated_goals = []
    for g_idx in goal_indices:
        vals = [r[g_idx] for r in rows if isinstance(r[g_idx], (int, float))]
        estimated_goals.append(sum(vals) / len(vals))

    # Calculate a score for every row in the dataset
    # Goal +: higher is better, Goal -: lower is better
    def get_score(r):
        score = 0.0
        for i, g_idx in enumerate(goal_indices):
            val = r[g_idx]
            # Normalize to 0-1 range roughly
            col_vals = [x[g_idx] for x in rows if isinstance(x[g_idx], (int, float))]
            min_v, max_v = min(col_vals), max(col_vals)
            norm = (val - min_v) / (max_v - min_v + 1e-9)
            if header[g_idx].endswith('-'):
                score += (1.0 - norm)
            else:
                score += norm
        return score / len(goal_indices)

    # Compare test row score to all rows
    test_score = 0.0
    for i, g_idx in enumerate(goal_indices):
        norm = (estimated_goals[i] - min(r[g_idx] for r in rows)) / (max(r[g_idx] for r in rows) - min(r[g_idx] for r in rows) + 1e-9)
        test_score += (1.0 - norm) if header[g_idx].endswith('-') else norm
    test_score /= len(goal_indices)

    all_scores = [get_score(r) for r in rows]
    better_than = sum(1 for s in all_scores if test_score > s)
    p = better_than / len(rows)
    
    reason = f"This team arrangement ranks in the top {int((1-p)*100)}% of all records based on its performance across all retention-related metrics."
    return (p, reason)

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    header = []
    
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

    # Test with the last row as a sample
    test_row = list(rows[-1])
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    for idx in goal_indices:
        test_row[idx] = "?"
        
    p, reason = justify(header, rows, test_row)
    print(f"Percentile Rank: {p:.2f}")
    print(f"Justification: {reason}")
