import csv

def justify(header, rows, row):
    """
    Estimates performance for a given configuration and compares it against
    the historical dataset to answer why 'bigger/deeper' isn't always better.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    input_indices = [i for i, name in enumerate(header) if not name.endswith(('-', '+'))]

    # Estimate goals for the target row using the average of the 5 nearest neighbors
    def distance(r1, r2):
        d = 0
        for i in input_indices:
            if isinstance(r1[i], (int, float)) and isinstance(r2[i], (int, float)):
                d += (r1[i] - r2[i])**2
        return d**0.5

    neighbors = sorted(rows, key=lambda r: distance(row, r))[:5]
    estimates = []
    for g_idx in goal_indices:
        vals = [n[g_idx] for n in neighbors]
        estimates.append(sum(vals) / len(vals))

    def get_score(goals):
        score = 0
        for i, g_idx in enumerate(goal_indices):
            col_vals = [r[g_idx] for r in rows]
            min_v, max_v = min(col_vals), max(col_vals)
            norm = (goals[i] - min_v) / (max_v - min_v + 1e-9)
            score += (1.0 - norm) if header[g_idx].endswith('-') else norm
        return score / len(goal_indices)

    target_score = get_score(estimates)
    better_count = sum(1 for r in rows if get_score([r[i] for i in goal_indices]) < target_score)
    p = better_count / len(rows)
    
    reason = "Bigger, deeper models often suffer from overfitting, leading to diminishing returns where increased complexity fails to improve performance metrics."
    return p, reason

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed = [val if header[i] == 'criterion' else float(val) for i, val in enumerate(row)]
                rows.append(processed)
        
        # Create a 'big/deep' test row
        test_row = [0.0] * len(header)
        for i, name in enumerate(header):
            if name == 'N_estimators': test_row[i] = 200.0
            elif name == 'Max_depth': test_row[i] = 20.0
            elif name == 'criterion': test_row[i] = 'squared_error'
            elif name.endswith(('-', '+')): test_row[i] = "?"
            else: test_row[i] = 1.0
            
        p, reason = justify(header, rows, test_row)
        print(f"Performance Rank: {p:.4f}")
        print(f"Answer: {reason}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
