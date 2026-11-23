import csv
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

def fix(header, row, levers):
    """
    Finds the best change to the provided levers to minimize 'Idle-'.
    Uses a Random Forest surrogate model trained on the full dataset.
    """
    filename = 'pom3a.n1000.train.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header_csv = next(reader)
        rows = []
        for r in reader:
            rows.append([float(val) for val in r])
    
    df = pd.DataFrame(rows, columns=header_csv)
    inputs = [c for c in header_csv if not (c.endswith(('-', '+')))]
    
    # Train surrogate model to predict 'Idle-'
    model = RandomForestRegressor(n_estimators=20, random_state=42)
    model.fit(df[inputs], df['Idle-'])
    
    best_change = {}
    best_idle = float('inf')
    
    # Try perturbations for each lever
    for col, bounds in levers.items():
        idx = header.index(col)
        
        # Generate test values
        if isinstance(bounds, (tuple, list)) and len(bounds) == 2:
            low, high = bounds
            test_vals = np.linspace(low, high, 5)
        else:
            test_vals = bounds
            
        for val in test_vals:
            new_row = list(row)
            new_row[idx] = val
            
            # Predict 'Idle-'
            pred = model.predict([new_row[:len(inputs)]])[0]
            if pred < best_idle:
                best_idle = pred
                best_change = {col: val}
                
    return best_change

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(val) for val in r] for r in reader]
        
        # Identify a "bad" row (high Idle-)
        df = pd.DataFrame(rows, columns=header)
        bad_row = rows[df['Idle-'].idxmax()]
        
        # Levers excluding 'Team Size' as per customer request
        levers = {
            'Culture': (0.0, 1.0),
            'Criticality': (0.0, 1.0),
            'Initial Known': (0.0, 1.0),
            'Inter-Dependency': (0.0, 1.0),
            'Dynamism': (0.0, 1.0),
            'Size': (0.0, 1.0),
            'Plan': (0.0, 1.0)
        }
        
        recommendation = fix(header, bad_row, levers)
        
        print("Customer Inquiry: I cannot hire. What else can I change to cut idle time?")
        print("Recommendation: To reduce idle time, we suggest the following adjustment:")
        for col, val in recommendation.items():
            print(f"  - {col}: set to {val:.4f}")
        print("This change is predicted to minimize idle time without requiring additional staff.")
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
