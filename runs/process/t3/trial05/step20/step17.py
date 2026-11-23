import csv
import random
import numpy as np
from sklearn.ensemble import RandomForestRegressor

def choose(header, rows, label):
    """
    Finds the best setup for a large, high-criticality project.
    We filter for rows where 'Size' and 'Criticality' are high,
    then use a surrogate model to optimize within that subset.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
    input_indices = [i for i, h in enumerate(header) if not h.endswith(('-', '+'))]
    
    # Identify indices for filtering
    size_idx = header.index('Size')
    crit_idx = header.index('Criticality')
    
    # Filter for "large and high criticality" (top 25% in both)
    # We use the available input data to find candidates
    candidates = [i for i, r in enumerate(rows) 
                  if r[size_idx] > 0.75 and r[crit_idx] > 0.75]
    
    # If not enough candidates, fallback to all
    if len(candidates) < 20:
        candidates = list(range(len(rows)))
        
    labeled = {} # index: score

    def get_score(row_goals):
        score = 0
        for i, val in enumerate(row_goals):
            if header[goal_indices[i]].endswith('-'):
                score -= val
            else:
                score += val
        return score

    # 1. Sample 20 candidates to build initial model
    sample_size = min(20, len(candidates))
    sample = random.sample(candidates, sample_size)
    for i in sample:
        labeled[i] = get_score(label(i))
        
    # 2. Iterative improvement (30 more labels)
    for _ in range(30):
        if len(labeled) >= 50: break
        
        X = [[rows[i][j] for j in input_indices] for i in labeled.keys()]
        y = list(labeled.values())
        model = RandomForestRegressor(n_estimators=20, random_state=42).fit(X, y)
        
        best_idx, best_pred = -1, -float('inf')
        for i in candidates:
            if i not in labeled:
                pred = model.predict([[rows[i][j] for j in input_indices]])[0]
                if pred > best_pred:
                    best_pred, best_idx = pred, i
        
        if best_idx != -1:
            labeled[best_idx] = get_score(label(best_idx))
            
    return max(labeled, key=labeled.get)

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            data = [[float(x) for x in r] for r in reader]
        
        true_goals = [[r[i] for i, h in enumerate(header) if h.endswith(('-', '+'))] for r in data]
        masked_rows = [[("?" if h.endswith(('-', '+')) else r[i]) for i, h in enumerate(header)] for r in data]
        
        def label(i): return true_goals[i]
        
        best_idx = choose(header, masked_rows, label)
        print(f"Customer Inquiry: Best setup for a large, high-criticality project?")
        print(f"Analysis: After evaluating candidates, the optimal configuration is at index {best_idx}.")
        print("This setup balances performance goals while accounting for project scale and risk.")
        exit(0)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
