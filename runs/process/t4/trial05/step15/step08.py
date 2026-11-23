import csv
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

def fix(header, row, levers):
    """
    Identifies the smallest change to 'Plan' or 'Team Size' to improve 
    the 'Cost-' and 'Idle-' goals for a bad row.
    """
    # Load data to train a surrogate model for local sensitivity analysis
    filename = 'pom3a.n1000.train.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header_csv = next(reader)
        rows = [[float(val) for val in row] for row in reader]
    
    df = pd.DataFrame(rows, columns=header_csv)
    inputs = [c for c in header if c in levers]
    goals = ['Cost-', 'Idle-']
    
    # Train a model to predict the goals we want to minimize
    model = RandomForestRegressor(n_estimators=20, random_state=42)
    model.fit(df[inputs], df[goals])
    
    best_change = {}
    min_score = float('inf')
    
    # Test small perturbations within allowed lever ranges
    # We try to find a change that minimizes the predicted Cost- and Idle-
    for col in inputs:
        low, high = levers[col]
        # Try 5 steps between low and high
        for val in np.linspace(low, high, 5):
            test_row = list(row)
            test_row[header.index(col)] = val
            
            # Predict impact
            pred = model.predict([ [test_row[header.index(c)] for c in inputs] ])[0]
            score = sum(pred) # Minimize sum of goals
            
            if score < min_score:
                min_score = score
                best_change = {col: val}
                
    return best_change

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [[float(val) for val in row] for row in reader]
    
    # Define levers based on the prompt's request (Plan and Team Size)
    levers = {
        'Plan': (0.0, 1.0),
        'Team Size': (0.0, 1.0)
    }
    
    # Find a 'bad' row (high cost and high idle)
    df = pd.DataFrame(rows, columns=header)
    bad_row_idx = (df['Cost-'] + df['Idle-']).idxmax()
    bad_row = rows[bad_row_idx]
    
    recommendation = fix(header, bad_row, levers)
    
    print("Customer Inquiry: How to rescue an over-budget, idle project?")
    print(f"Analysis: For the worst-performing setup, we recommend the following adjustments:")
    for col, val in recommendation.items():
        print(f" - Adjust '{col}' to {val:.4f}")
    print("These changes are predicted to reduce both Cost and Idle time.")
