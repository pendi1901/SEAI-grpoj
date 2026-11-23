import csv
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

def fix(header, row, levers):
    """
    Recommends changes to a 'bad' row to improve its performance.
    Uses a Random Forest model trained on the dataset to predict the impact
    of changing levers on the composite goal score.
    """
    # Load data to build a surrogate model
    filename = 'pom3a.n1000.train.csv'
    df = pd.read_csv(filename)
    
    input_cols = [c for c in header if not (c.endswith('-') or c.endswith('+'))]
    goal_cols = [c for c in header if c.endswith('-') or c.endswith('+')]
    
    # Create a composite score (normalized)
    scores = pd.DataFrame(index=df.index)
    for goal in goal_cols:
        col = df[goal]
        if goal.endswith('-'):
            scores[goal] = (col.max() - col) / (col.max() - col.min())
        else:
            scores[goal] = (col - col.min()) / (col.max() - col.min())
    df['composite'] = scores.mean(axis=1)
    
    # Train model
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(df[input_cols], df['composite'])
    
    # Find the best lever change
    best_change = {}
    best_score = -1
    
    # Try changing each lever to its bounds or midpoint
    for col, bounds in levers.items():
        col_idx = header.index(col)
        original_val = row[col_idx]
        
        # Test extreme values
        for val in [bounds[0], bounds[1]]:
            if val == original_val: continue
            
            test_row = list(row)
            test_row[col_idx] = val
            
            # Predict score
            pred = model.predict([test_row[:len(input_cols)]])[0]
            if pred > best_score:
                best_score = pred
                best_change = {col: val}
                
    return best_change

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [ [float(x) for x in r] for r in reader ]

    # Define levers based on the problem domain (numeric ranges)
    levers = {
        'Plan': (0.0, 1.0),
        'Team Size': (0.0, 1.0),
        'Size': (0.0, 1.0)
    }
    
    # Pick a 'bad' row (e.g., one with high Cost- or Idle-)
    # Here we pick the row with the highest Cost-
    cost_idx = header.index('Cost-')
    bad_row = max(rows, key=lambda r: r[cost_idx])
    
    recommendation = fix(header, bad_row, levers)
    
    print("Customer Inquiry: How to rescue an over-budget, idle project?")
    print(f"Analysis: To improve performance, we recommend adjusting the following:")
    for col, val in recommendation.items():
        print(f"  Change '{col}' to {val:.4f}")
    print("This adjustment is predicted to improve the overall project efficiency.")
    exit(0)
