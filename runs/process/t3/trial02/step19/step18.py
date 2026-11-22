import csv
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

def fix(header, row, levers):
    """
    Identifies the best change to non-hiring levers to minimize 'Idle-'.
    We use a Random Forest to predict 'Idle-' and perform a local search
    over the allowed lever ranges.
    """
    # Load data to train a surrogate model
    filename = 'pom3a.n1000.train.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header_data = next(reader)
        rows = []
        for r in reader:
            rows.append([float(val) if val.replace('.', '', 1).isdigit() or 
                         (val.startswith('-') and val[1:].replace('.', '', 1).isdigit()) 
                         else val for val in r])
    
    df = pd.DataFrame(rows, columns=header_data)
    goals = [c for c in header_data if c.endswith('-') or c.endswith('+')]
    inputs = [c for c in header_data if c not in goals]
    
    # Train model to predict Idle-
    X = df[inputs]
    y = df['Idle-']
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    best_change = {}
    best_idle = float('inf')
    
    # Search for the best lever adjustment
    for col, allowed in levers.items():
        if isinstance(allowed, tuple):
            low, high = allowed
            # Test 10 points in the range
            test_values = np.linspace(low, high, 10)
        else:
            test_values = allowed
            
        for val in test_values:
            temp_row = list(row)
            temp_row[header.index(col)] = val
            
            # Predict Idle- for this change
            pred_idle = model.predict([temp_row[:len(inputs)]])[0]
            
            if pred_idle < best_idle:
                best_idle = pred_idle
                best_change = {col: val}
                
    return best_change

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
        
        # Find a row with high idle time
        df = pd.DataFrame(rows, columns=header)
        bad_row = rows[df['Idle-'].idxmax()]
        
        # Levers excluding 'Team Size' (hiring)
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
        print("Analysis: We analyzed the project factors and recommend the following adjustment:")
        for col, val in recommendation.items():
            print(f"- Adjust '{col}' to {val:.4f}")
        print("This change is predicted to reduce idle time by optimizing project parameters.")
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
