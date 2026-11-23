import csv
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor

def justify(header, rows, row):
    """
    Estimates the performance of a given row and returns its percentile rank
    relative to the provided dataset.
    """
    df = pd.DataFrame(rows, columns=header)
    goals = [c for c in header if c.endswith('-') or c.endswith('+')]
    inputs = [c for c in header if c not in goals]

    # 1. Estimate the missing goal values for the target row
    X_train = df[inputs]
    y_train = df[goals]
    
    # Simple KNN to estimate goals
    model = KNeighborsRegressor(n_neighbors=5)
    model.fit(X_train, y_train)
    
    # Create a temporary row for prediction (replace '?' with mean of inputs for safety)
    # or just use the provided row's inputs
    input_vals = [row[i] for i in range(len(header)) if header[i] in inputs]
    estimated_goals = model.predict([input_vals])[0]
    
    # 2. Calculate scores for all rows (including the estimated one)
    def calculate_score(row_goals):
        scores = []
        for i, goal_name in enumerate(goals):
            col = df[goal_name]
            val = row_goals[i]
            norm = (val - col.min()) / (col.max() - col.min() + 1e-9)
            scores.append(1 - norm if goal_name.endswith('-') else norm)
        return sum(scores) / len(scores)

    all_scores = [calculate_score(r[i] for i, h in enumerate(header) if h in goals) for r in rows]
    target_score = calculate_score(estimated_goals)
    
    # 3. Calculate percentile
    better_than = [s for s in all_scores if target_score > s]
    p = len(better_than) / len(all_scores)
    
    reason = f"This setup is estimated to outperform {p:.1%} of all possible configurations based on its projected goal metrics."
    return p, reason

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) if i < len(header) - 3 or (i >= len(header) - 3 and val.replace('.','',1).isdigit()) else val for i, val in enumerate(row)])
        
        # Pick a sample row and mask its goals
        sample_row = list(rows[0])
        for i, h in enumerate(header):
            if h.endswith('-') or h.endswith('+'):
                sample_row[i] = "?"
        
        p, reason = justify(header, rows, sample_row)
        print(f"Percentile: {p}")
        print(f"Reason: {reason}")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
