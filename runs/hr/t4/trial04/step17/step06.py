import csv
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def justify(header, rows, row):
    """
    Estimates the performance of a given row against historical data.
    Returns (p, reason) where p is the fraction of rows that 'row' is better than.
    """
    # Identify goal column
    goal_col = next(c for c in header if c.endswith('+') or c.endswith('-'))
    goal_idx = header.index(goal_col)
    
    # Prepare training data
    df = pd.DataFrame(rows, columns=header)
    X = df.drop(columns=[goal_col])
    y = df[goal_col]
    
    # Encode symbolic columns consistently
    encoders = {}
    for col in X.columns:
        if X[col].dtype == 'object':
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            encoders[col] = le
        else:
            X[col] = X[col].astype(float)
            
    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Prepare input row
    input_df = pd.DataFrame([row], columns=header).drop(columns=[goal_col])
    for col in input_df.columns:
        if col in encoders:
            input_df[col] = encoders[col].transform(input_df[col].astype(str))
        else:
            input_df[col] = input_df[col].astype(float)
            
    pred = model.predict(input_df)[0]
    
    # Calculate fraction of rows that 'row' is better than
    history = [r[goal_idx] for r in rows]
    if goal_col.endswith('+'):
        better_than = [h for h in history if pred > h]
    else:
        better_than = [h for h in history if pred < h]
        
    p = len(better_than) / len(history)
    reason = f"This arrangement is predicted to perform better than {p:.1%} of historical records regarding {goal_col}."
    
    return (p, reason)

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed_row)
    
    # Test with the first row, masking its goal
    test_row = list(rows[0])
    goal_idx = next(i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-'))
    test_row[goal_idx] = "?"
    
    p, reason = justify(header, rows, test_row)
    print(f"Rank: {p:.4f}")
    print(f"Reason: {reason}")
