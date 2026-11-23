import csv

def justify(header, rows, row):
    """
    Estimates the performance of 'row' by comparing its input features to the 
    historical 'rows' using a K-Nearest Neighbors approach, then calculates 
    the percentile rank of the estimated performance.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    input_indices = [i for i, name in enumerate(header) if i not in goal_indices]

    def get_dist(r1, r2):
        d = 0
        for i in input_indices:
            v1, v2 = r1[i], r2[i]
            if isinstance(v1, str):
                d += 0 if v1 == v2 else 1
            else:
                d += (v1 - v2) ** 2
        return d ** 0.5

    def get_score(r):
        # Normalize goals: MRE- (min), ACC+ (max), PRED40+ (max)
        scores = []
        for idx in goal_indices:
            vals = [x[idx] for x in rows]
            mn, mx = min(vals), max(vals)
            norm = (r[idx] - mn) / (mx - mn) if mx > mn else 0
            scores.append(1.0 - norm if header[idx].endswith('-') else norm)
        return sum(scores) / len(scores)

    # Estimate goals for the target row using 5-NN
    distances = sorted([(get_dist(row, r), r) for r in rows])
    k = 5
    neighbors = distances[:k]
    
    estimated_goals = []
    for idx in goal_indices:
        avg = sum(n[1][idx] for n in neighbors) / k
        estimated_goals.append(avg)
    
    # Create a temporary row with estimated goals to score it
    row_with_goals = list(row)
    for i, idx in enumerate(goal_indices):
        row_with_goals[idx] = estimated_goals[i]
    
    target_score = get_score(row_with_goals)
    
    # Compare against all rows
    all_scores = [get_score(r) for r in rows]
    better_than = [s for s in all_scores if target_score > s]
    p = len(better_than) / len(rows)
    
    reason = f"This configuration is estimated to outperform {p:.1%} of historical setups based on its input parameters."
    return p, reason

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed = [float(val) if header[i] not in ['criterion'] else val 
                             for i, val in enumerate(row)]
                rows.append(processed)
        
        # Test with the last row as the target
        target = list(rows[-1])
        for i in range(len(header)):
            if header[i].endswith(('-', '+')):
                target[i] = "?"
        
        p, reason = justify(header, rows, target)
        print(reason)
        exit(0)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
