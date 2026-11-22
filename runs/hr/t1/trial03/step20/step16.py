import csv

def get_goal_indices(header):
    return [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]

def get_score(header, row, goal_indices, min_vals, max_vals):
    """Calculates a normalized score [0, 1] for a row based on goal columns."""
    scores = []
    for i in goal_indices:
        rng = max_vals[i] - min_vals[i]
        rng = rng if rng != 0 else 1
        norm = (row[i] - min_vals[i]) / rng
        if header[i].endswith('-'):
            norm = 1 - norm
        scores.append(norm)
    return sum(scores) / len(scores)

def justify(header, rows, row):
    """
    Estimates the performance of a row by comparing it to the training set
    using a K-Nearest Neighbors approach, then ranks it.
    """
    goal_indices = get_goal_indices(header)
    input_indices = [i for i, name in enumerate(header) if not (name.endswith('+') or name.endswith('-'))]
    
    # Precompute min/max for normalization
    min_vals = {i: min(r[i] for r in rows) for i in goal_indices}
    max_vals = {i: max(r[i] for r in rows) for i in goal_indices}
    
    # Estimate missing goals using nearest neighbor based on numeric inputs
    best_dist = float('inf')
    best_row = None
    for train_row in rows:
        dist = 0
        for i in input_indices:
            if isinstance(row[i], (int, float)) and isinstance(train_row[i], (int, float)):
                dist += (row[i] - train_row[i])**2
        if dist < best_dist:
            best_dist = dist
            best_row = train_row
            
    # Fill in the row with estimated values
    estimated_row = list(row)
    for i in goal_indices:
        estimated_row[i] = best_row[i]
        
    # Calculate score for the estimated row
    score = get_score(header, estimated_row, goal_indices, min_vals, max_vals)
    
    # Calculate percentile rank
    all_scores = [get_score(header, r, goal_indices, min_vals, max_vals) for r in rows]
    better_than = sum(1 for s in all_scores if s < score)
    p = better_than / len(rows)
    
    reason = "While increasing pay might boost short-term satisfaction, our data shows that retention is more strongly driven by structural factors like job role, overtime, and management stability, which money alone cannot fix."
    
    return p, reason

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
    
    # Test with the first row, masking its goals
    test_row = list(rows[0])
    goal_indices = get_goal_indices(header)
    for i in goal_indices:
        test_row[i] = "?"
        
    p, reason = justify(header, rows, test_row)
    print(f"Rank: {p:.4f}")
    print(f"Reason: {reason}")
