import csv
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from step01 import remember

def fix(header, row, levers):
    """
    Identifies the most impactful lever to change to improve the row's performance.
    Uses a Random Forest to predict the impact of changing levers on the aggregate goal.
    """
    # 1. Load data to build a surrogate model
    filename = 'pom3a.n1000.train.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header_csv = next(reader)
        rows = [[float(val) for val in row] for row in reader]
    
    df = pd.DataFrame(rows, columns=header_csv)
    inputs = [c for c in header if c in levers]
    goals = [c for c in header if c.endswith(('-', '+'))]
    
    # 2. Calculate aggregate score for training
    scores = pd.DataFrame(index=df.index)
    for goal in goals:
        col_data = df[goal]
        norm = (col_data - col_data.min()) / (col_data.max() - col_data.min())
        scores[goal] = (1 - norm) if goal.endswith('-') else norm
    df['agg'] = scores.mean(axis=1)
    
    # 3. Train model
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(df[inputs], df['agg'])
    
    # 4. Evaluate changes for each lever
    best_change = {}
    best_score = -1
    
    current_row_df = pd.DataFrame([row], columns=header)
    
    for col, bounds in levers.items():
        # Try a few points in the range
        low, high = bounds
        for val in [low, (low + high) / 2, high]:
            test_row = current_row_df.copy()
            test_row[col] = val
            pred = model.predict(test_row[inputs])[0]
            if pred > best_score:
                best_score = pred
                best_change = {col: val}
                
    return best_change

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [[float(val) for val in row] for row in reader]
    
    # Define levers: Plan and Team Size are the primary project management controls
    levers = {
        'Plan': (0.0, 1.0),
        'Team Size': (0.0, 1.0)
    }
    
    # Pick a "bad" row (e.g., one with high cost and high idle)
    # Using the last row as a sample of a bad setup
    bad_row = rows[-1]
    
    recommendation = fix(header, bad_row, levers)
    
    print("To rescue this project from being over budget and idle:")
    for col, val in recommendation.items():
        print(f"Adjust '{col}' to {val:.4f}.")
    print("This change is predicted to improve the overall project efficiency.")
