import csv
from step01 import remember
from step02 import guess

def justify(header, rows, row):
    """
    Estimates the performance of the given row and compares it against the 
    historical dataset to justify its quality.
    """
    # 1. Estimate the missing goal values for the target row
    # We use the guess function from step02. 
    # Note: guess returns a list of estimates for the first goal (MRE-).
    # We need to estimate all goals. For simplicity, we use the logic 
    # that the row's performance is determined by its input similarity.
    
    # Create a temporary list containing the target row to use with guess
    test_rows = [row]
    # guess() in step02 only estimates the first goal (MRE-). 
    # We will use the average of the 5 nearest neighbors for all goals.
    input_indices = [i for i, h in enumerate(header) if not (h.endswith('-') or h.endswith('+'))]
    
    def get_dist(r1, r2):
        d = 0
        for i in input_indices:
            if isinstance(r1[i], str):
                d += 0 if r1[i] == r2[i] else 1
            else:
                d += abs(r1[i] - r2[i])
        return d

    # Find 5 nearest neighbors
    neighbors = sorted(rows, key=lambda r: get_dist(row, r))[:5]
    
    # Estimate goals (indices 0, 1, 2)
    estimated_goals = []
    for g_idx in range(3):
        estimated_goals.append(sum(n[g_idx] for n in neighbors) / 5)
    
    # 2. Calculate score for the target row
    def get_score(r):
        # Goals: MRE- (min), ACC+ (max), PRED40+ (max)
        # Normalize using global min/max
        scores = []
        for i in range(3):
            vals = [x[i] for x in rows]
            mn, mx = min(vals), max(vals)
            norm = (r[i] - mn) / (mx - mn) if mx > mn else 0
            scores.append(1 - norm if i == 0 else norm)
        return sum(scores)

    target_row_with_goals = row[:]
    for i in range(3):
        target_row_with_goals[i] = estimated_goals[i]
    
    target_score = get_score(target_row_with_goals)
    
    # 3. Compare against all rows
    all_scores = [get_score(r) for r in rows]
    better_than_count = sum(1 for s in all_scores if target_score > s)
    p = better_than_count / len(rows)
    
    reason = f"This setup outperforms {p:.1%} of historical configurations based on its estimated performance metrics."
    
    return p, reason

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rows.append([val if header[i] == 'criterion' else float(val) for i, val in enumerate(row)])
    
    # Pick a sample row and mask it
    sample_row = rows[0][:]
    for i in range(3):
        sample_row[i] = "?"
        
    p, reason = justify(header, rows, sample_row)
    print(f"Performance percentile: {p}")
    print(f"Justification: {reason}")
