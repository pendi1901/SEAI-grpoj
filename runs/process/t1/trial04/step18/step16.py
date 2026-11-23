import csv

def justify(header, rows, row):
    """
    Estimates the performance of a row by comparing it to the training set.
    Returns (p, reason) where p is the percentile rank and reason is a summary.
    """
    # Identify goal indices and directions
    goals = []
    for i, name in enumerate(header):
        if name.endswith('-') or name.endswith('+'):
            goals.append((i, name.endswith('-')))

    # Helper to calculate score (lower is better)
    def get_score(r):
        total = 0
        for col_idx, is_min in goals:
            val = float(r[col_idx])
            total += val if is_min else (1.0 - val)
        return total

    # Identify input indices
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    # Euclidean distance in input space
    def dist(r1, r2):
        d = 0
        for i in input_indices:
            d += (r1[i] - r2[i]) ** 2
        return d ** 0.5

    # Find 3 nearest neighbors to estimate the missing goal values
    neighbors = sorted(rows, key=lambda r: dist(row, r))[:3]
    
    # Estimate goal values for the target row
    estimated_row = list(row)
    for col_idx, _ in goals:
        estimated_row[col_idx] = sum(n[col_idx] for n in neighbors) / 3
    
    # Calculate score for the estimated row and all training rows
    target_score = get_score(estimated_row)
    all_scores = [get_score(r) for r in rows]
    
    # Calculate fraction of rows that are worse (i.e., have a higher penalty score)
    better_than_count = sum(1 for s in all_scores if s > target_score)
    p = better_than_count / len(rows)
    
    reason = f"This setup is estimated to outperform {p:.1%} of all known configurations, whereas the recommended setup achieves a higher performance tier."
    return p, reason

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        # Example: Compare a hypothetical setup B (row 0)
        test_row = list(rows[0])
        for i, name in enumerate(header):
            if name.endswith('-') or name.endswith('+'):
                test_row[i] = "?"
        
        p, reason = justify(header, rows, test_row)
        print(f"Percentile: {p:.4f}")
        print(f"Reason: {reason}")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
