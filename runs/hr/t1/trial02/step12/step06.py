import csv

def justify(header, rows, row):
    """
    Estimates the rank of a given row by comparing its predicted goal performance
    against the actual performance of the provided population.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    input_indices = [i for i, name in enumerate(header) if i not in goal_indices]

    # Simple KNN to estimate the missing goal values in 'row'
    def get_dist(r1, r2):
        d = 0
        for i in input_indices:
            if isinstance(r1[i], float) and isinstance(r2[i], float):
                d += (r1[i] - r2[i])**2
            else:
                d += 1 if r1[i] != r2[i] else 0
        return d**0.5

    # Estimate goals for the input row
    k = 7
    distances = sorted([(get_dist(row, r), r) for r in rows], key=lambda x: x[0])
    neighbors = distances[:k]
    
    estimates = []
    for g_idx in goal_indices:
        vals = [n[1][g_idx] for n in neighbors]
        estimates.append(sum(vals) / k)

    # Calculate score for the row (higher is better for + goals, lower for - goals)
    def score(r):
        s = 0
        for i, g_idx in enumerate(goal_indices):
            val = r[g_idx]
            if header[g_idx].endswith('+'):
                s += val
            else:
                s -= val
        return s

    target_score = sum(estimates[i] if header[goal_indices[i]].endswith('+') else -estimates[i] 
                       for i in range(len(goal_indices)))
    
    all_scores = [score(r) for r in rows]
    better_than = [s for s in all_scores if s < target_score]
    p = len(better_than) / len(rows)
    
    reason = f"This arrangement ranks in the top {int((1-p)*100)}% of all teams because it outperforms {int(p*100)}% of the existing staff records in tenure and retention metrics."
    
    return (p, reason)

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # Test with the first row, masking its goals
    test_row = list(rows[0])
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    for idx in goal_indices:
        test_row[idx] = "?"
        
    p, reason = justify(header, rows, test_row)
    print(f"Rank: {p:.4f}")
    print(f"Justification: {reason}")
