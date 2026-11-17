import csv

def justify(header, rows, row):
    """
    Returns (p, reason) where p is the percentile rank of the row
    and reason explains its relative performance.
    """
    goals = []
    for i, name in enumerate(header):
        if name.endswith('-') or name.endswith('+'):
            goals.append((i, name.endswith('-')))

    def get_score(r):
        score = 0.0
        for idx, is_min in goals:
            val = float(r[idx])
            # Normalize column values to [0, 1]
            col_vals = [float(row[idx]) for row in rows]
            low, high = min(col_vals), max(col_vals)
            span = (high - low) if high > low else 1.0
            norm = (val - low) / span
            score += (norm if is_min else (1.0 - norm))
        return score / len(goals)

    # We need to estimate the goal values for the target row.
    # Using the average of the dataset as a proxy for the unknown "?" values.
    estimated_row = list(row)
    for idx, is_min in goals:
        col_vals = [float(r[idx]) for r in rows]
        estimated_row[idx] = sum(col_vals) / len(col_vals)

    target_score = get_score(estimated_row)
    all_scores = [get_score(r) for r in rows]
    
    # Count how many rows are worse (have a higher score) than the target
    better_than_count = sum(1 for s in all_scores if s > target_score)
    p = better_than_count / len(all_scores)
    
    reason = f"This configuration outperforms {p:.1%} of all available setups based on its projected multi-objective performance."
    return p, reason

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.train.csv"
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rows.append(row)
    
    # Pick a sample row to justify (e.g., the 100th row)
    sample_row = list(rows[100])
    for i, name in enumerate(header):
        if name.endswith('-') or name.endswith('+'):
            sample_row[i] = "?"
            
    p, reason = justify(header, rows, sample_row)
    print(f"Justification: {reason}")
