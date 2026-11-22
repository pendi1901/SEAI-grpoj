import csv
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

def fix(header, row, levers):
    """
    Recommends a change to a bad row to reduce 'Idle-' without hiring (Team Size).
    Uses a Random Forest to predict the impact of changing available levers.
    """
    filename = 'pom3a.n1000.train.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header_csv = next(reader)
        rows = []
        for r in reader:
            rows.append([float(x) for x in r])
    
    df = pd.DataFrame(rows, columns=header_csv)
    
    # Identify inputs and the target goal
    inputs = [c for c in header if c in levers]
    target = 'Idle-'
    
    # Train model to predict 'Idle-' (lower is better)
    X = df[inputs]
    y = df[target]
    model = RandomForestRegressor(n_estimators=20, random_state=42)
    model.fit(X, y)
    
    best_change = {}
    best_score = float('inf')
    
    # Try perturbations for allowed levers
    for col, bounds in levers.items():
        idx = header.index(col)
        original_val = row[idx]
        
        # Test 5 points within the allowed range
        low, high = bounds
        for val in np.linspace(low, high, 5):
            if val == original_val: continue
            
            test_row = list(row)
            test_row[idx] = val
            
            # Predict Idle-
            test_x = pd.DataFrame([test_row], columns=header)[inputs]
            score = model.predict(test_x)[0]
            
            if score < best_score:
                best_score = score
                best_change = {col: val}
                
    return best_change

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(x) for x in r] for r in reader]
        
        # Customer cannot hire (Team Size is excluded from levers)
        # We allow changing Plan, Size, Dynamism, etc.
        levers = {
            'Plan': (0.0, 1.0),
            'Size': (0.0, 1.0),
            'Dynamism': (0.0, 1.0),
            'Culture': (0.0, 1.0)
        }
        
        # Pick a "bad" row (high Idle-)
        df = pd.DataFrame(rows, columns=header)
        bad_row = df.nlargest(1, 'Idle-').iloc[0].tolist()
        
        recommendation = fix(header, bad_row, levers)
        
        print("Customer Inquiry: I cannot hire. What else can I change to cut idle time?")
        print("Analysis: To reduce idle time without changing team size, we recommend:")
        for col, val in recommendation.items():
            print(f"- {col}: Adjust to {val:.4f}")
        print("These adjustments are predicted to optimize workflow and reduce idle capacity.")
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
