import csv
import random

def choose(header, rows, label):
    """
    Finds a setup that is both high-performing and 'small'.
    We define 'small' as having a low N_estimators value.
    We sample 50 rows, score them based on performance and size,
    and return the index of the best one.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    n_idx = header.index('N_estimators')
    
    # Sample 50 indices
    indices = random.sample(range(len(rows)), min(50, len(rows)))
    
    labeled_data = []
    for i in indices:
        goals = label(i)
        labeled_data.append((i, goals))
    
    # Normalize goals and size
    def normalize(val, min_v, max_v, reverse=False):
        if max_v == min_v: return 0.5
        norm = (val - min_v) / (max_v - min_v)
        return (1 - norm) if reverse else norm

    goal_vals = {idx: [d[1][i] for d in labeled_data] for i, idx in enumerate(goal_indices)}
    mins = {idx: min(vals) for idx, vals in goal_vals.items()}
    maxs = {idx: max(vals) for idx, vals in goal_vals.items()}
    
    n_vals = [rows[i][n_idx] for i in indices]
    min_n, max_n = min(n_vals), max(n_vals)
    
    best_idx = -1
    best_score = -1.0
    
    for i, goals in labeled_data:
        norm_scores = []
        for j, g_idx in enumerate(goal_indices):
            name = header[g_idx]
            reverse = name.endswith('-')
            norm_scores.append(normalize(goals[j], mins[g_idx], maxs[g_idx], reverse))
        
        # Performance score (average of goals)
        perf = sum(norm_scores) / len(norm_scores)
        # Size score (smaller N_estimators is better)
        size = normalize(rows[i][n_idx], min_n, max_n, True)
        
        # Combined score: 70% performance, 30% size
        total_score = (0.7 * perf) + (0.3 * size)
        
        if total_score > best_score:
            best_score = total_score
            best_idx = i
            
    return best_idx

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            true_goals = []
            for row in reader:
                processed_row = []
                goals = []
                for i, val in enumerate(row):
                    if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 
                                     'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                        processed_row.append(float(val))
                    else:
                        processed_row.append(val)
                    
                    if header[i].endswith('-') or header[i].endswith('+'):
                        goals.append(float(val))
                
                rows.append(processed_row)
                true_goals.append(goals)

        masked_rows = []
        for r in rows:
            new_r = [("?" if header[i].endswith('-') or header[i].endswith('+') else r[i]) for i in range(len(r))]
            masked_rows.append(new_r)

        def label(i):
            return true_goals[i]

        best_idx = choose(header, masked_rows, label)
        print(f"Recommended setup for nightly runs found at index {best_idx}.")
        print(f"Setup details: {rows[best_idx]}")
        exit(0)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
