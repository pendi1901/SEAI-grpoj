import csv
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsRegressor

def choose(header, rows, label):
    """
    Selects the best row by using an active learning approach:
    1. Sample a small initial set to train a surrogate model.
    2. Use the model to predict performance on remaining rows.
    3. Query the most promising rows (Expected Improvement or best predicted).
    4. Return the index of the best row found after 50 labels.
    """
    goals = [c for c in header if c.endswith('-') or c.endswith('+')]
    inputs = [c for c in header if c not in goals]
    
    # Convert rows to DataFrame for easier handling
    df = pd.DataFrame(rows, columns=header)
    X = df[inputs].values
    
    # Keep track of labeled data
    labeled_indices = []
    
    def get_score(goal_values):
        # Normalize goals: lower is better for all
        # Since we don't have the full dataset distribution here, 
        # we use the values returned by label() to compute a relative score.
        # However, for simplicity, we treat the goal vector as a point to minimize.
        score = 0
        for i, g in enumerate(goals):
            val = goal_values[i]
            if g.endswith('+'):
                score -= val  # Maximize
            else:
                score += val  # Minimize
        return score

    # Initial sampling: 10 random rows to build a baseline
    np.random.seed(42)
    indices_to_sample = np.random.choice(len(rows), 10, replace=False).tolist()
    
    best_idx = -1
    best_score = float('inf')
    
    # Main loop: 50 labels allowed
    for _ in range(50):
        # Label the selected indices
        for idx in indices_to_sample:
            if idx not in labeled_indices:
                goal_vals = label(idx)
                score = get_score(goal_vals)
                if score < best_score:
                    best_score = score
                    best_idx = idx
                labeled_indices.append(idx)
        
        if len(labeled_indices) >= 50:
            break
            
        # Train model on labeled data
        X_train = [rows[i][:len(inputs)] for i in labeled_indices]
        y_train = [label(i) for i in labeled_indices]
        
        knn = KNeighborsRegressor(n_neighbors=3)
        knn.fit(X_train, y_train)
        
        # Predict on all rows
        preds = knn.predict(X)
        scores = [get_score(p) for p in preds]
        
        # Pick the next best candidate that hasn't been labeled
        remaining = [i for i in range(len(rows)) if i not in labeled_indices]
        if not remaining:
            break
        
        # Strategy: pick the one with the best predicted score
        next_idx = remaining[np.argmin([scores[i] for i in remaining])]
        indices_to_sample = [next_idx]
        
    return best_idx

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) if val.replace('.', '', 1).isdigit() or 
                             (val.startswith('-') and val[1:].replace('.', '', 1).isdigit()) 
                             else val for val in row])
        
        # Keep a copy of true goals for the label function
        true_goals = [row[len(header)-3:] for row in rows]
        
        def label(i):
            return true_goals[i]
            
        best_idx = choose(header, rows, label)
        print(f"The best configuration found is at index {best_idx}.")
        print(f"Performance metrics: {true_goals[best_idx]}")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
