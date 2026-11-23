import csv
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def fix(header, row, levers):
    """
    Recommends changes to a 'bad' row to improve its goal columns.
    We simulate changes for each lever and pick the one that results
    in the best predicted outcome.
    """
    goal_col = next(c for c in header if c.endswith('+') or c.endswith('-'))
    is_maximize = goal_col.endswith('+')
    
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header_full = next(reader)
        for r in reader:
            rows.append([float(val) if header_full[i][0].isupper() else val for i, val in enumerate(r)])
    
    df = pd.DataFrame(rows, columns=header)
    X = df.drop(columns=[goal_col])
    y = df[goal_col]
    
    encoders = {}
    for col in X.columns:
        if X[col].dtype == 'object':
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            encoders[col] = le
        else:
            X[col] = X[col].astype(float)
            
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    best_val = -float('inf') if is_maximize else float('inf')
    best_change = {}
    
    for col, allowed in levers.items():
        idx = header.index(col)
        original_val = row[idx]
        
        test_vals = []
        if isinstance(allowed, tuple):
            test_vals = [allowed[0], allowed[1], (allowed[0] + allowed[1]) / 2]
        else:
            test_vals = allowed
            
        for val in test_vals:
            if val == original_val: continue
            
            temp_row = list(row)
            temp_row[idx] = val
            
            input_df = pd.DataFrame([temp_row], columns=header).drop(columns=[goal_col])
            for c in input_df.columns:
                if c in encoders:
                    input_df[c] = encoders[c].transform(input_df[c].astype(str))
                else:
                    input_df[c] = input_df[c].astype(float)
            
            pred = model.predict(input_df)[0]
            
            if (is_maximize and pred > best_val) or (not is_maximize and pred < best_val):
                best_val = pred
                best_change = {col: val}
                
    return best_change

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rows.append([float(val) if header[i][0].isupper() else val for i, val in enumerate(row)])
            
    bad_row = rows[1]
    levers = {
        'businessTravel': ['Non-Travel', 'Travel_Rarely', 'Travel_Frequently'],
        'overTime': ['No', 'Yes'],
        'TrainingTimesLastYear': (0.0, 6.0),
        'PercentSalaryHike': (11.0, 25.0),
        'StockOptionLevel': (0.0, 3.0)
    }
    
    recommendation = fix(header, bad_row, levers)
    print(f"Recommendation for improvement: {recommendation}")
