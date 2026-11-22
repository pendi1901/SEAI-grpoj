import csv
import random

def choose(header, rows, label):
    """
    Finds a setup that balances performance (goals) and size (N_estimators).
    We use a budget of 50 labels to perform a greedy search, sampling 50 rows
    and picking the best one based on a multi-objective score that penalizes
    large N_estimators.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
    n_idx = header.index('N_estimators')
    
    # We have a budget of 50 labels. We will sample 50 rows, label them,
    # and pick the best one.
    sample_size = 50
    indices = random.sample(range(len(rows)), min(sample_size, len(rows)))
    
    labeled_data = []
    for i in indices:
        goals = label(i)
        labeled_data.append((goals, i))
    
    # To score, we need to normalize the goals and N_estimators across our sample.
    # Goals: MRE- (min), ACC+ (max), PRED40+ (max)
    # N_estimators: (min)
    
    def get_score(goals, n_val):
        # Extract values for normalization
        all_mre = [d[0][0] for d in labeled_data]
        all_acc = [d[0][1] for d in labeled_data]
        all_pred = [d[0][2] for d in labeled_data]
        all_n = [rows[d[1]][n_idx] for d in labeled_data]
        
        def norm(val, vals):
            mn, mx = min(vals), max(vals)
            return (val - mn) / (mx - mn) if mx > mn else 0
        
        # Score = (1 - norm_mre) + norm_acc + norm_pred - norm_n
        s = (1 - norm(goals[0], all_mre)) + norm(goals[1], all_acc) + \
            norm(goals[2], all_pred) - norm(n_val, all_n)
        return s

    best_idx = -1
    best_score = -float('inf')
    
    for goals, idx in labeled_data:
        s = get_score(goals, rows[idx][n_idx])
        if s > best_score:
            best_score = s
            best_idx = idx
            
    return best_idx

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    rows = []
    header = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [val if header[i] == 'criterion' else float(val) 
                             for i, val in enumerate(row)]
            rows.append(processed_row)

    # Store true values to simulate the label function
    true_goals = []
    for r in rows:
        true_goals.append([r[i] for i, h in enumerate(header) if h.endswith(('-', '+'))])
        # Hide goals
        for i, h in enumerate(header):
            if h.endswith(('-', '+')):
                r[i] = "?"

    def label(i):
        return true_goals[i]

    best_idx = choose(header, rows, label)
    
    print(f"Recommended setup found at row index: {best_idx}")
    print(f"Configuration: {rows[best_idx]}")
    print(f"This setup balances high forecast accuracy with a smaller model size (N_estimators).")
