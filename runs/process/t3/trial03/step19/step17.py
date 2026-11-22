import csv
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

def choose(header, rows, label):
    """
    Finds the best setup for a 'large' project (high 'Size') using 
    active learning with a budget of 50 trials.
    """
    goal_cols = [c for c in header if c.endswith('-') or c.endswith('+')]
    input_cols = [c for c in header if c not in goal_cols]
    
    # Filter for 'large' projects (Size > median)
    size_idx = header.index('Size')
    large_indices = [i for i, row in enumerate(rows) if row[size_idx] > 0.5]
    
    # If no large projects, fall back to all
    search_space = large_indices if large_indices else list(range(len(rows)))
    
    labeled = {}
    
    def get_agg(row_goals):
        scores = []
        for i, col in enumerate(goal_cols):
            val = row_goals[i]
            # Normalize: '-' minimized (1-val), '+' maximized (val)
            scores.append(1.0 - val if col.endswith('-') else val)
        return np.mean(scores)

    # 1. Initial exploration: 10 random samples from the search space
    np.random.seed(42)
    to_sample = np.random.choice(search_space, min(10, len(search_space)), replace=False).tolist()
    
    # 2. Iterative refinement: up to 50 queries total
    for _ in range(50):
        if not to_sample:
            break
            
        idx = to_sample.pop(0)
        if idx not in labeled:
            labeled[idx] = label(idx)
        
        if len(labeled) >= 50:
            break
            
        # Train surrogate on labeled data
        X = pd.DataFrame([[rows[i][header.index(c)] for c in input_cols] for i in labeled], columns=input_cols)
        y = [get_agg(labeled[i]) for i in labeled]
        
        model = RandomForestRegressor(n_estimators=20, random_state=42).fit(X, y)
        
        # Predict for remaining candidates
        unlabeled = [i for i in search_space if i not in labeled]
        if not unlabeled:
            break
            
        X_unlabeled = pd.DataFrame([[rows[i][header.index(c)] for c in input_cols] for i in unlabeled], columns=input_cols)
        preds = model.predict(X_unlabeled)
        
        # Pick best predicted
        best_pred_idx = unlabeled[np.argmax(preds)]
        to_sample.append(best_pred_idx)
        
    # Return index of the best labeled row
    best_idx = max(labeled, key=lambda i: get_agg(labeled[i]))
    return best_idx

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            full_data = []
            for row in reader:
                full_data.append([float(val) if val.replace('.', '', 1).isdigit() or 
                                 (val.startswith('-') and val[1:].replace('.', '', 1).isdigit()) 
                                 else val for val in row])
        
        rows = []
        for row in full_data:
            new_row = row[:]
            for i, col in enumerate(header):
                if col.endswith('-') or col.endswith('+'):
                    new_row[i] = "?"
            rows.append(new_row)
            
        def label(i):
            goals = [c for c in header if c.endswith('-') or c.endswith('+')]
            return [float(full_data[i][header.index(c)]) for c in goals]
        
        best_idx = choose(header, rows, label)
        print(f"Best setup for large, high-stakes projects found at index: {best_idx}")
        print("This setup was identified using a targeted search of 50 trials.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
