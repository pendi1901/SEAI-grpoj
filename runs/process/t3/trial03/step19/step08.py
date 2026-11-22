import csv
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

def fix(header, row, levers):
    """
    Recommends changes to a bad row to improve its goals.
    Uses a Random Forest to identify which lever change yields the best 
    predicted improvement in the aggregate goal score.
    """
    # Load data to build a surrogate model
    filename = 'pom3a.n1000.train.csv'
    df = pd.read_csv(filename)
    
    goals = [c for c in header if c.endswith('-') or c.endswith('+')]
    inputs = [c for c in header if c not in goals]
    
    # Normalize goals for aggregate score
    def get_agg(r):
        scores = []
        for col in goals:
            vals = df[col]
            norm = (r[col] - vals.min()) / (vals.max() - vals.min() + 1e-9)
            scores.append(1 - norm if col.endswith('-') else norm)
        return np.mean(scores)

    # Train model to predict aggregate score
    df['aggregate'] = df.apply(get_agg, axis=1)
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(df[inputs], df['aggregate'])
    
    best_change = {}
    best_score = -1
    
    # Evaluate each lever
    for col, bounds in levers.items():
        if col not in header: continue
        
        # Test a few values within the range
        test_vals = []
        if isinstance(bounds, list): # Symbolic
            test_vals = bounds
        else: # Numeric (low, high)
            test_vals = [bounds[0], (bounds[0] + bounds[1]) / 2, bounds[1]]
            
        for val in test_vals:
            temp_row = dict(zip(header, row))
            temp_row[col] = val
            
            # Predict score
            input_vec = pd.DataFrame([temp_row])[inputs]
            pred_score = model.predict(input_vec)[0]
            
            if pred_score > best_score:
                best_score = pred_score
                best_change = {col: val}
                
    return best_change

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    df = pd.read_csv(filename)
    header = df.columns.tolist()
    rows = df.values.tolist()
    
    # Find a "bad" row (high cost, high idle)
    # We define bad as having above-average Cost- and Idle-
    bad_rows = df[(df['Cost-'] > df['Cost-'].mean()) & (df['Idle-'] > df['Idle-'].mean())]
    bad_row = bad_rows.iloc[0].tolist()
    
    # Define levers: Plan and Team Size are typical project management levers
    levers = {
        'Plan': (0.0, 1.0),
        'Team Size': (0.0, 1.0)
    }
    
    recommendation = fix(header, bad_row, levers)
    
    print("Customer Inquiry: How to rescue an over-budget, idle project?")
    print(f"Recommended change: {recommendation}")
    print("Rationale: This adjustment is predicted to improve the project's overall efficiency score.")
