import csv
import random

def get_score(header, goals):
    """
    Calculates a normalized aggregate score for a row.
    Goals: MRE- (minimize), ACC+ (maximize), PRED40+ (maximize).
    Score = (1 - MRE) + ACC + PRED
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    # Normalize: (1 - MRE) + ACC + PRED
    # Assuming values are in [0, 1]
    mre = goals[0]
    acc = goals[1]
    pred = goals[2]
    return (1.0 - mre) + acc + pred

def choose(header, rows, label):
    """
    Finds a setup that forecasts well (high score) and is small (low N_estimators).
    We use a multi-objective approach: maximize (Score - weight * N_estimators).
    """
    n_idx = header.index('N_estimators')
    
    # Normalize N_estimators to [0, 1] for the trade-off
    all_n = [float(r[n_idx]) for r in rows]
    min_n, max_n = min(all_n), max(all_n)
    
    def get_combined_score(i, goals):
        score = get_score(header, goals)
        n_val = float(rows[i][n_idx])
        # Normalize N_estimators: lower is better
        norm_n = (n_val - min_n) / (max_n - min_n + 1e-9)
        # Weight: balance performance (score) vs size (norm_n)
        # We want high score and low norm_n
        return score - (0.2 * norm_n)

    best_idx = -1
    best_val = -float('inf')
    
    # Sample 50 rows to find the best trade-off
    indices = list(range(len(rows)))
    random.shuffle(indices)
    
    for i in indices[:50]:
        goals = label(i)
        val = get_combined_score(i, goals)
        if val > best_val:
            best_val = val
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
                processed = []
                goals = []
                for i, val in enumerate(row):
                    if header[i].endswith('-') or header[i].endswith('+'):
                        goals.append(float(val))
                        processed.append("?")
                    else:
                        try: processed.append(float(val))
                        except ValueError: processed.append(val)
                rows.append(processed)
                true_goals.append(goals)

        queries = set()
        def label(i):
            if i not in queries:
                if len(queries) >= 50:
                    raise Exception("Budget exceeded")
                queries.add(i)
            return true_goals[i]

        best_idx = choose(header, rows, label)
        print(f"Optimization complete. Best compact setup found at index: {best_idx}")
        print(f"This setup balances high forecasting accuracy with low computational overhead.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
