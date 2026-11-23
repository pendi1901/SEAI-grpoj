import csv
import step01
import step02

def justify(header, rows, row):
    """
    Estimates the performance of 'row' using the nearest neighbor from 'rows',
    then calculates the percentile rank of this estimate against all 'rows'.
    """
    # 1. Estimate the goals for the '?' row
    # We use the guess logic from step02 to predict the goals
    # Since step02 only predicts MRE-, we extend the logic to all goals
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    input_indices = [i for i, h in enumerate(header) if not (h.endswith('-') or h.endswith('+'))]
    
    def dist(r1, r2):
        d = 0
        for i in input_indices:
            v1, v2 = r1[i], r2[i]
            if isinstance(v1, float):
                d += (v1 - v2) ** 2
            else:
                d += 0 if v1 == v2 else 1
        return d ** 0.5

    # Find nearest neighbor to estimate goals
    best_d = float('inf')
    neighbor = None
    for r in rows:
        d = dist(row, r)
        if d < best_d:
            best_d = d
            neighbor = r
    
    # Estimated goals for the input row
    est_goals = [neighbor[i] for i in goal_indices]
    
    # 2. Calculate how many rows are worse than this estimate
    # A row is better if it has a higher composite score
    # We use the scoring logic from step01
    def get_score(r_goals):
        scores = []
        for i, g_idx in enumerate(goal_indices):
            col_vals = [row[g_idx] for row in rows]
            min_v, max_v = min(col_vals), max(col_vals)
            val = r_goals[i]
            norm = (val - min_v) / (max_v - min_v) if max_v != min_v else 0.5
            # If ends in -, minimize (1-norm), if +, maximize (norm)
            scores.append(1 - norm if header[g_idx].endswith('-') else norm)
        return sum(scores) / len(scores)

    est_score = get_score(est_goals)
    all_scores = [get_score([r[i] for i in goal_indices]) for r in rows]
    
    better_than_count = sum(1 for s in all_scores if est_score > s)
    p = better_than_count / len(rows)
    
    reason = f"This setup is estimated to outperform {p:.1%} of all configurations based on its similarity to high-performing historical data."
    return (p, reason)

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                processed = [float(val) if header[i] not in ['criterion'] else val 
                             for i, val in enumerate(row)]
                rows.append(processed)
        
        # Test with the last row, masking its goals
        test_row = list(rows[-1])
        for i in range(len(test_row)):
            if header[i].endswith('-') or header[i].endswith('+'):
                test_row[i] = "?"
        
        p, reason = justify(header, rows, test_row)
        print(f"Justification: {reason}")
        print(f"Percentile: {p:.4f}")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
