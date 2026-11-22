import csv
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsRegressor

def justify(header, rows, row):
    """
    Estimates the goals for the given row using KNN, then calculates its 
    percentile rank against the provided dataset.
    """
    df = pd.DataFrame(rows, columns=header)
    goals = [c for c in header if c.endswith('-') or c.endswith('+')]
    inputs = [c for c in header if c not in goals]

    # 1. Estimate goals for the input row
    X_train = df[inputs]
    y_train = df[goals]
    model = KNeighborsRegressor(n_neighbors=5)
    model.fit(X_train, y_train)
    
    # Extract inputs from the provided row
    row_inputs = [row[i] for i, col in enumerate(header) if col in inputs]
    estimated_goals = model.predict([row_inputs])[0]

    # 2. Calculate aggregate scores for all rows
    def get_aggregate(r_goals):
        scores = []
        for i, col in enumerate(goals):
            vals = df[col]
            # Normalize to [0, 1]
            norm = (r_goals[i] - vals.min()) / (vals.max() - vals.min() + 1e-9)
            scores.append(1 - norm if col.endswith('-') else norm)
        return np.mean(scores)

    # Calculate score for the estimated row
    row_score = get_aggregate(estimated_goals)
    
    # Calculate scores for all existing rows
    all_scores = [get_aggregate(r[goals].tolist()) for _, r in df.iterrows()]
    
    # 3. Calculate percentile rank (fraction of rows better than this one)
    # A row is better if its score is higher
    better_than = [s for s in all_scores if s < row_score]
    p = len(better_than) / len(all_scores)
    
    reason = f"This setup is estimated to be better than {p:.1%} of all known configurations based on its input parameters."
    
    return p, reason

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
        
        # Example: Compare a specific setup (e.g., row 1)
        test_row = rows[1].copy()
        for i, col in enumerate(header):
            if col.endswith('-') or col.endswith('+'):
                test_row[i] = "?"
        
        p, reason = justify(header, rows, test_row)
        print(f"Rank: {p:.4f}")
        print(f"Reason: {reason}")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
