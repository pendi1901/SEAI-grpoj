import csv
import random

def choose(header, rows, label):
    """
    Finds a setup that balances performance (goals) and efficiency (small size).
    We use a budget of 50 labels to sample the space, then pick the best row
    based on a multi-objective score that penalizes large N_estimators.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    n_est_idx = header.index('N_estimators')
    
    # Budget: 50 labels
    indices = random.sample(range(len(rows)), 50)
    
    best_idx = -1
    best_score = -float('inf')
    
    # Collect data for normalization
    sampled_goals = []
    for idx in indices:
        sampled_goals.append(label(idx))
        
    # Calculate global min/max for goals from samples
    goal_mins = [min(s[j] for s in sampled_goals) for j in range(len(goal_indices))]
    goal_maxs = [max(s[j] for s in sampled_goals) for j in range(len(goal_indices))]
    
    # Normalize N_estimators to penalize large values
    n_ests = [rows[idx][n_est_idx] for idx in indices]
    n_min, n_max = min(n_ests), max(n_ests)
    
    for i, idx in enumerate(indices):
        goals = sampled_goals[i]
        
        # Performance score
        perf_score = 0
        for j, g_idx in enumerate(goal_indices):
            val = goals[j]
            rng = goal_maxs[j] - goal_mins[j] + 1e-9
            norm = (val - goal_mins[j]) / rng
            if header[g_idx].endswith('-'):
                perf_score -= norm
            else:
                perf_score += norm
        
        # Efficiency score: smaller N_estimators is better
        n_val = rows[idx][n_est_idx]
        n_norm = (n_val - n_min) / (n_max - n_min + 1e-9)
        efficiency_score = -n_norm
        
        # Combined score (weighting performance higher)
        total_score = (0.7 * perf_score) + (0.3 * efficiency_score)
        
        if total_score > best_score:
            best_score = total_score
            best_idx = idx
            
    return best_idx

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    header = []
    
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                processed_row = []
                for i, val in enumerate(row):
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)
        
        def label(i):
            return [rows[i][j] for j, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
        
        best_idx = choose(header, rows, label)
        print(f"Optimal setup found at index {best_idx}.")
        print("This setup balances high performance with a small footprint for nightly runs.")
        exit(0)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
