import csv
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsRegressor

def justify(header, rows, row):
    """
    Estimates the goal values for the provided row using KNN, then calculates
    the percentile rank of this row against the existing dataset.
    """
    df = pd.DataFrame(rows, columns=header)
    goals = [c for c in header if c.endswith('-') or c.endswith('+')]
    inputs = [c for c in header if c not in goals]
    
    # 1. Estimate goal values for the input row
    X_train = df[inputs]
    y_train = df[goals]
    knn = KNeighborsRegressor(n_neighbors=5)
    knn.fit(X_train, y_train)
    
    # Predict goals for the row (which has '?' in goal columns)
    row_inputs = [row[header.index(i)] for i in inputs]
    predicted_goals = knn.predict([row_inputs])[0]
    
    # 2. Calculate aggregate score for all rows
    # Normalize: lower is better for all (invert '+' goals)
    def get_scores(data_df):
        scores = pd.DataFrame(index=data_df.index)
        for i, goal in enumerate(goals):
            col = data_df[goal]
            norm = (col - col.min()) / (col.max() - col.min() + 1e-9)
            if goal.endswith('+'):
                norm = 1 - norm
            scores[goal] = norm
        return scores.sum(axis=1)

    all_scores = get_scores(df)
    
    # Calculate score for the target row
    row_norm_scores = []
    for i, goal in enumerate(goals):
        col = df[goal]
        val = predicted_goals[i]
        norm = (val - col.min()) / (col.max() - col.min() + 1e-9)
        if goal.endswith('+'):
            norm = 1 - norm
        row_norm_scores.append(norm)
    row_score = sum(row_norm_scores)
    
    # 3. Calculate percentile (fraction of rows that are worse than this one)
    # A row is better if its score is lower
    better_than_count = (all_scores > row_score).sum()
    p = better_than_count / len(df)
    
    reason = f"This configuration is estimated to outperform {p:.1%} of all possible setups based on its predicted performance metrics."
    
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
        
        # Test with the first row, masking its goals
        test_row = rows[0].copy()
        for i, col in enumerate(header):
            if col.endswith('-') or col.endswith('+'):
                test_row[i] = '?'
        
        p, reason = justify(header, rows, test_row)
        print(f"Percentile: {p:.4f}")
        print(f"Justification: {reason}")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
