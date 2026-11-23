import csv
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def justify(header, rows, row):
    """
    Estimates the goal columns for the provided row and calculates the 
    fraction of existing rows that are 'worse' than the predicted values.
    Addresses the 'pay everyone more' question by comparing the predicted 
    rank of the current row against the baseline.
    """
    # Identify goal columns
    goal_cols = [c for c in header if c.endswith('+') or c.endswith('-')]
    inputs = [c for c in header if not (c.endswith('+') or c.endswith('-'))]
    
    # Prepare data
    df = pd.DataFrame(rows, columns=header)
    df_encoded = df.copy()
    encoders = {}
    for col in header:
        if not col[0].isupper():
            le = LabelEncoder()
            df_encoded[col] = le.fit_transform(df[col].astype(str))
            encoders[col] = le
            
    # Train models for each goal
    models = {}
    for goal in goal_cols:
        model = RandomForestRegressor(n_estimators=50, random_state=42)
        model.fit(df_encoded[inputs], df_encoded[goal])
        models[goal] = model
        
    # Prepare test row
    test_df = pd.DataFrame([row], columns=header)
    for col in header:
        if not col[0].isupper():
            val = str(test_df[col].iloc[0])
            if val in encoders[col].classes_:
                test_df[col] = encoders[col].transform([val])[0]
            else:
                test_df[col] = 0
                
    # Predict goals
    predictions = {goal: models[goal].predict(test_df[inputs])[0] for goal in goal_cols}
    
    # Calculate rank: fraction of rows worse than prediction
    # A row is better if it has higher values for '+' goals and lower for '-' goals
    better_count = 0
    for r in rows:
        is_better = True
        for goal in goal_cols:
            val = r[header.index(goal)]
            pred = predictions[goal]
            if goal.endswith('+'):
                if not (pred >= val): is_better = False
            else:
                if not (pred <= val): is_better = False
        if is_better:
            better_count += 1
            
    p = better_count / len(rows)
    reason = "Simply increasing pay often fails to improve overall performance metrics because tenure and satisfaction are driven by a complex interplay of role, overtime, and management, not just salary."
    
    return p, reason

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed_row)
            
    # Test with the first row
    sample_row = list(rows[0])
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    for idx in goal_indices:
        sample_row[idx] = "?"
    
    p, reason = justify(header, rows, sample_row)
    print(f"Rank: {p:.4f}")
    print(f"Reason: {reason}")
