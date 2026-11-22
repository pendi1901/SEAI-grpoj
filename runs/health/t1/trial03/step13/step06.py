import csv

def justify(header, rows, row):
    """
    Estimates the performance of 'row' by comparing it to its k-nearest neighbors
    in 'rows', then calculates the fraction of 'rows' that are worse than 'row'.
    """
    # Identify indices
    goal_indices = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
    input_indices = [i for i, h in enumerate(header) if not h.endswith(('-', '+'))]
    
    # Normalize numeric inputs for distance
    numeric_inputs = [i for i in input_indices if header[i] != 'criterion']
    mins = [min(r[i] for r in rows) for i in numeric_inputs]
    maxs = [max(r[i] for r in rows) for i in numeric_inputs]
    
    def get_dist(r1, r2):
        d = 0
        for idx, i in enumerate(numeric_inputs):
            rng = maxs[idx] - mins[idx]
            if rng > 0:
                d += ((r1[i] - r2[i]) / rng) ** 2
        for i in input_indices:
            if header[i] == 'criterion' and r1[i] != r2[i]:
                d += 1
        return d**0.5

    # Estimate goal values for the target row using k-NN
    k = 10
    distances = sorted([(get_dist(row, r), r) for r in rows], key=lambda x: x[0])
    neighbors = [d[1] for d in distances[:k]]
    
    estimated_goals = []
    for g_idx in goal_indices:
        estimated_goals.append(sum(n[g_idx] for n in neighbors) / k)
    
    # Compare estimated row against all rows
    def is_better(r_goals, target_goals):
        # A row is better if it dominates or has a better aggregate score
        # Here we use a simple normalized score: lower MRE is better, higher others are better
        def score(goals):
            s = 0
            for i, g_idx in enumerate(goal_indices):
                col = header[g_idx]
                vals = [r[g_idx] for r in rows]
                mn, mx = min(vals), max(vals)
                norm = (goals[i] - mn) / (mx - mn) if mx > mn else 0
                s += (1 - norm) if col.endswith('-') else norm
            return s
        return score(target_goals) > score(r_goals)

    better_count = sum(1 for r in rows if is_better(r, estimated_goals))
    p = better_count / len(rows)
    
    reason = f"This setup outperforms {p:.1%} of all historical configurations based on its estimated multi-objective performance."
    return p, reason

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rows.append([val if header[i] == 'criterion' else float(val) for i, val in enumerate(row)])
    
    # Test with the last row as a hidden query
    test_row = list(rows[-1])
    for i in range(len(header)):
        if header[i].endswith(('-', '+')):
            test_row[i] = "?"
            
    p, reason = justify(header, rows[:-1], test_row)
    print(f"Score: {p:.4f}")
    print(f"Justification: {reason}")
