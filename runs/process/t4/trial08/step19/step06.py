import csv
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from step01 import remember

def justify(header, rows, row):
    """
    Estimates the performance of a row and returns its percentile rank
    and a justification string.
    """
    df = pd.DataFrame(rows, columns=header)
    inputs = [col for col in header if not (col.endswith('-') or col.endswith('+'))]
    goals = [col for col in header if col.endswith(('-', '+'))]
    
    # Estimate the goals for the provided row using KNN
    knn = KNeighborsRegressor(n_neighbors=5)
    knn.fit(df[inputs], df[goals])
    
    # Extract inputs from the provided row (which has '?' for goals)
    input_vals = [row[i] for i, col in enumerate(header) if col in inputs]
    estimated_goals = knn.predict([input_vals])[0]
    
    # Calculate aggregate score for all rows
    def get_agg(data):
        scores = pd.DataFrame(index=data.index)
        for i, goal in enumerate(goals):
            col_data = data[goal].astype(float)
            norm = (col_data - col_data.min()) / (col_data.max() - col_data.min() + 1e-9)
            scores[goal] = 1 - norm if goal.endswith('-') else norm
        return scores.mean(axis=1)

    all_scores = get_agg(df)
    
    # Calculate score for the estimated row
    # We normalize the estimated goal using the training data's min/max
    est_scores = []
    for i, goal in enumerate(goals):
        col_data = df[goal].astype(float)
        val = estimated_goals[i]
        norm = (val - col_data.min()) / (col_data.max() - col_data.min() + 1e-9)
        est_scores.append(1 - norm if goal.endswith('-') else norm)
    
    row_score = np.mean(est_scores)
    
    # Calculate percentile (fraction of rows worse than this one)
    p = (all_scores < row_score).mean()
    
    reason = f"This setup is estimated to outperform {p:.1%} of all known configurations based on its input parameters."
    return p, reason

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        # Pick a sample row and mask its goals to test the justification
        test_row = list(rows[0])
        goal_indices = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
        for idx in goal_indices:
            test_row[idx] = "?"
            
        p, reason = justify(header, rows, test_row)
        print(f"Justification: {reason}")
        print(f"Percentile rank: {p:.4f}")
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
