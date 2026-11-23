import csv
import random

def choose(header, rows, label):
    """
    Finds a setup that balances performance (MRE-, ACC+, PRED40+) 
    with 'smallness' (N_estimators, Max_depth).
    We use a budget of 50 labels to sample the space and optimize.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    n_est_idx = header.index('N_estimators')
    depth_idx = header.index('Max_depth')

    # Sample 50 random rows
    indices = random.sample(range(len(rows)), 50)
    
    # Store labeled data
    data = []
    for i in indices:
        goals = label(i)
        data.append({'idx': i, 'goals': goals, 'row': rows[i]})

    # Normalize goals and inputs for scoring
    # Goals: MRE- (min), ACC+ (max), PRED40+ (max)
    # Smallness: N_estimators (min), Max_depth (min)
    
    def get_score(item):
        g = item['goals']
        r = item['row']
        
        # Normalize goals (0 to 1)
        mre_norm = 1.0 - (g[0] / 1.0) # Assume range 0-1
        acc_norm = g[1] / 1.0
        pred_norm = g[2] / 1.0
        
        # Normalize smallness (0 to 1, lower is better)
        # N_estimators range ~50-200, Max_depth ~1-20
        n_est_norm = 1.0 - ((r[n_est_idx] - 50) / 150)
        depth_norm = 1.0 - ((r[depth_idx] - 1) / 19)
        
        # Weighted score: 60% performance, 40% smallness
        perf = (mre_norm + acc_norm + pred_norm) / 3.0
        small = (n_est_norm + depth_norm) / 2.0
        return (0.6 * perf) + (0.4 * small)

    best_idx = -1
    best_score = -1.0
    
    for item in data:
        score = get_score(item)
        if score > best_score:
            best_score = score
            best_idx = item['idx']
            
    return best_idx

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            true_goals = []
            for row in reader:
                # Store true goals
                true_goals.append([float(row[0]), float(row[1]), float(row[2])])
                # Process row
                processed = [val if header[i] == 'criterion' else float(val) for i, val in enumerate(row)]
                # Mask goals
                for idx in [0, 1, 2]: processed[idx] = "?"
                rows.append(processed)

        def label(i):
            return true_goals[i]

        best_idx = choose(header, rows, label)
        print(f"Recommended setup: Row index {best_idx}")
        print(f"This configuration balances high predictive accuracy with a compact model size.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
