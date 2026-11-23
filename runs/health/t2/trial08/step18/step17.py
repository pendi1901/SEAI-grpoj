import csv
from step01 import remember
from step02 import guess

def choose(header, rows, label):
    """
    Finds a setup that balances performance (goals) and size (N_estimators).
    We label 50 rows, then select the one that maximizes a composite score
    of performance and smallness.
    """
    n = len(rows)
    # Sample 50 rows spread across the dataset
    indices_to_label = [int(i * (n / 50)) for i in range(50)]
    
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    n_est_idx = header.index('N_estimators')
    
    labeled_data = []
    for i in indices_to_label:
        true_goals = label(i)
        row_with_goals = list(rows[i])
        for j, g_idx in enumerate(goal_indices):
            row_with_goals[g_idx] = true_goals[j]
        labeled_data.append(row_with_goals)
    
    # Score: Performance (from remember) + Smallness (inverse of N_estimators)
    # We normalize N_estimators to [0, 1] where smaller is better
    n_ests = [r[n_est_idx] for r in labeled_data]
    min_n, max_n = min(n_ests), max(n_ests)
    
    def get_smallness(val):
        if max_n == min_n: return 1.0
        return 1.0 - ((val - min_n) / (max_n - min_n))
    
    # Get performance scores from remember
    perf_scores = {}
    best_indices = remember(header, labeled_data)
    for idx, score in enumerate(best_indices):
        # remember returns indices of top 5%, we map back to labeled_data index
        perf_scores[idx] = 1.0
        
    best_overall_idx = -1
    best_total_score = -1.0
    
    for i, row in enumerate(labeled_data):
        perf = perf_scores.get(i, 0.5) # Default to 0.5 if not in top 5%
        small = get_smallness(row[n_est_idx])
        # Composite score: 70% performance, 30% smallness
        total = (0.7 * perf) + (0.3 * small)
        if total > best_total_score:
            best_total_score = total
            best_overall_idx = indices_to_label[i]
            
    return best_overall_idx

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            true_goals_map = {}
            for i, row in enumerate(reader):
                processed = []
                goals = []
                for j, val in enumerate(row):
                    if header[j] == 'criterion':
                        processed.append(val)
                    elif header[j].endswith('-') or header[j].endswith('+'):
                        processed.append("?")
                        goals.append(float(val))
                    else:
                        processed.append(float(val))
                rows.append(processed)
                true_goals_map[i] = goals
        
        def label(i):
            return true_goals_map[i]
            
        best_pos = choose(header, rows, label)
        print(f"Analysis complete. The best setup for performance and nightly runtime is at index {best_pos}.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
