import csv
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

def fix(header, row, levers):
    """
    Finds the smallest change to levers to improve Cost- and Idle- goals.
    """
    filename = 'pom3a.n1000.train.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header_csv = next(reader)
        rows = [[float(val) for val in r] for r in reader]
    
    df = pd.DataFrame(rows, columns=header_csv)
    goals = [c for c in header_csv if c.endswith(('-', '+'))]
    inputs = [c for c in header_csv if c not in goals]
    
    # Train models to predict goals
    models = {}
    for goal in goals:
        m = RandomForestRegressor(n_estimators=20, random_state=42)
        m.fit(df[inputs], df[goal])
        models[goal] = m
        
    def get_score(r_list):
        # r_list is a list of values in header order
        r_df = pd.DataFrame([r_list], columns=header)
        scores = [models[g].predict(r_df[inputs])[0] for g in goals]
        return sum(scores)

    best_change = {}
    best_score = get_score(row)
    
    for col, bounds in levers.items():
        idx = header.index(col)
        low, high = bounds
        # Test a few points in the range
        for val in [low, (low + high) / 2, high]:
            new_row = list(row)
            new_row[idx] = val
            new_score = get_score(new_row)
            
            if new_score < best_score:
                best_score = new_score
                best_change = {col: val}
                
    return best_change

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(val) for val in r] for r in reader]
        
        df = pd.DataFrame(rows, columns=header)
        # Identify a "bad" row (high cost/idle)
        bad_row = df.loc[df[['Cost-', 'Idle-']].sum(axis=1).idxmax()].tolist()
        
        levers = {
            'Plan': (0.0, 1.0),
            'Team Size': (0.0, 1.0)
        }
        
        recommendation = fix(header, bad_row, levers)
        
        print("Customer Inquiry: How to rescue the project?")
        if recommendation:
            for col, val in recommendation.items():
                print(f"Recommendation: Adjust '{col}' to {val:.4f}.")
        else:
            print("No significant improvement found with current levers.")
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
