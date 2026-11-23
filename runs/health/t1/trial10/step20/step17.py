import csv
import random

def choose(header, rows, label):
    """
    Finds a setup that balances performance (MRE-, ACC+, PRED40+) 
    with efficiency (small N_estimators).
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    n_est_idx = header.index('N_estimators')
    
    # We want to maximize: (1 - MRE) + ACC + PRED - (N_estimators / 200)
    # This penalizes large N_estimators to favor "small enough to run every night".
    def get_score(row, goals):
        mre, acc, pred = goals
        # Normalize goals to [0, 1]
        score = (1.0 - mre) + acc + pred
        # Penalty for size: N_estimators ranges roughly 50-200
        size_penalty = row[n_est_idx] / 200.0
        return score - size_penalty

    # Sample 50 random indices to find the best balance
    indices = random.sample(range(len(rows)), min(50, len(rows)))
    
    best_idx = -1
    best_score = float('-inf')
    
    for i in indices:
        goals = label(i)
        score = get_score(rows[i], goals)
        if score > best_score:
            best_score = score
            best_idx = i
            
    return best_idx

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            all_rows = []
            true_goals = []
            for row in reader:
                processed = [float(val) if header[i] not in ['criterion'] else val 
                             for i, val in enumerate(row)]
                goals = [processed[i] for i, name in enumerate(header) if name.endswith(('-', '+'))]
                true_goals.append(goals)
                
                masked = list(processed)
                for i in range(len(header)):
                    if header[i].endswith(('-', '+')):
                        masked[i] = "?"
                all_rows.append(masked)

        def label(i):
            return true_goals[i]

        best_index = choose(header, all_rows, label)
        
        print(f"Recommended setup found at index {best_index}.")
        print(f"This setup balances high predictive accuracy with a smaller model size for nightly runs.")
        print(f"Performance metrics: MRE={true_goals[best_index][0]:.4f}, ACC={true_goals[best_index][1]:.4f}, PRED40={true_goals[best_index][2]:.4f}")
        exit(0)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
