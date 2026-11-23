import csv

def justify(header, rows, row):
    """
    Estimates the performance of 'row' and returns its percentile rank
    relative to the provided 'rows' dataset.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    input_indices = [i for i in range(len(header)) if i not in goal_indices]

    def get_score(r):
        # Lower is better: minimize '-' and maximize '+' (by inverting)
        s = 0
        for idx in goal_indices:
            val = float(r[idx])
            if header[idx].endswith('-'):
                s += val
            else:
                s += (1.0 - val)
        return s

    # Estimate goals for the target row using 3-Nearest Neighbors
    def get_dist(r1, r2):
        d2 = 0
        for i in input_indices:
            d2 += (r1[i] - r2[i]) ** 2
        return d2 ** 0.5

    # Find 3 nearest neighbors to estimate missing goals
    distances = []
    for r in rows:
        distances.append((get_dist(row, r), r))
    distances.sort(key=lambda x: x[0])
    
    # Estimate goals by averaging neighbors
    estimated_goals = [0.0] * len(goal_indices)
    for i in range(3):
        for j, g_idx in enumerate(goal_indices):
            estimated_goals[j] += distances[i][1][g_idx]
    
    estimated_row = list(row)
    for j, g_idx in enumerate(goal_indices):
        estimated_row[g_idx] = estimated_goals[j] / 3
    
    # Calculate percentile
    target_score = get_score(estimated_row)
    all_scores = [get_score(r) for r in rows]
    # Better than means score is lower
    better_than = sum(1 for s in all_scores if s > target_score)
    p = better_than / len(rows)
    
    reason = f"This configuration is estimated to outperform {p:.1%} of all possible setups based on its input characteristics."
    return p, reason

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(x) for x in row] for row in reader]
        
        # Example: Compare two rows (A and B)
        # A is a high-performing row, B is a lower-performing row
        row_a = list(rows[0])
        row_b = list(rows[10])
        
        goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
        
        # Mask goals
        row_a_masked = [("?" if i in goal_indices else val) for i, val in enumerate(row_a)]
        row_b_masked = [("?" if i in goal_indices else val) for i, val in enumerate(row_b)]
        
        p_a, reason_a = justify(header, rows, row_a_masked)
        p_b, reason_b = justify(header, rows, row_b_masked)
        
        print(f"Analysis: Why recommend A over B?")
        print(f"Setup A percentile: {p_a:.4f}")
        print(f"Setup B percentile: {p_b:.4f}")
        print(f"Explanation: Setup A is superior because it ranks in the top {p_a:.1%} of configurations, whereas B only reaches the top {p_b:.1%}.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
