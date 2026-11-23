import csv
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

def fix(header, row, levers):
    """
    Finds the best change to the provided levers to minimize 'Idle-'.
    """
    filename = 'pom3a.n1000.train.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header_csv = next(reader)
        rows = []
        for r in reader:
            rows.append([float(val) for val in r])
    
    df = pd.DataFrame(rows, columns=header_csv)
    inputs = [col for col in header if not (col.endswith('-') or col.endswith('+'))]
    target = 'Idle-'
    
    # Train a surrogate model to predict 'Idle-'
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(df[inputs], df[target])
    
    best_val = None
    best_col = None
    min_idle = float('inf')
    
    # Test perturbations for each lever
    for col, bounds in levers.items():
        idx = header.index(col)
        low, high = bounds
        
        # Test 10 points within the lever range
        for val in np.linspace(low, high, 10):
            new_row = list(row)
            new_row[idx] = val
            
            # Predict Idle-
            input_row = [new_row[i] for i, h in enumerate(header) if h in inputs]
            pred_idle = model.predict([input_row])[0]
            
            if pred_idle < min_idle:
                min_idle = pred_idle
                best_col = col
                best_val = val
                
    return {best_col: best_val}

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(val) for val in r] for r in reader]
        
        # Identify a "bad" row (high idle time)
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
        print("Analysis: We modeled the impact of non-hiring levers on idle time.")
        for col, val in recommendation.items():
            print(f"Recommendation: Adjust '{col}' to {val:.4f}.")
        print("Conclusion: This change is predicted to reduce idle time without requiring new staff.")
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
