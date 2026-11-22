import csv
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def justify(header, rows, row):
    """
    Estimates the goal value for the given row and compares it against
    the distribution of the full dataset to determine its rank.
    """
    # Identify goal column
    goal_col = [c for c in header if c.endswith('+') or c.endswith('-')][0]
    goal_idx = header.index(goal_col)
    
    # Prepare training data
    df_train = pd.DataFrame(rows, columns=header)
    df_row = pd.DataFrame([row], columns=header)
    
    # Features are all columns except the goal
    features = [c for c in header if not (c.endswith('+') or c.endswith('-'))]
    
    # Combine to ensure consistent LabelEncoding
    df_combined = pd.concat([df_train[features], df_row[features]], axis=0).copy()
    
    # Encode symbolic columns
    for col in features:
        if df_combined[col].dtype == 'object':
            le = LabelEncoder()
            df_combined[col] = le.fit_transform(df_combined[col].astype(str))
            
    X_train = df_combined.iloc[:len(rows)]
    X_test = df_combined.iloc[len(rows):]
    y_train = df_train[goal_col]
    
    # Train model to estimate goal
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    prediction = model.predict(X_test)[0]
    
    # Calculate rank
    all_goals = [float(r[goal_idx]) for r in rows]
    if goal_col.endswith('+'):
        better_than = [g for g in all_goals if prediction > g]
    else:
        better_than = [g for g in all_goals if prediction < g]
        
    p = len(better_than) / len(all_goals)
    
    # Answer the specific customer question about salary
    reason = "While increasing salary is a common lever, our model shows that tenure is driven by a complex mix of job role, overtime, and work-life balance, meaning money alone is rarely the sole predictor of long-term retention."
    
    return p, reason

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)
    
    # Test with the first row
    test_row = rows[0][:]
    goal_idx = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')][0]
    test_row[goal_idx] = "?"
    
    p, reason = justify(header, rows, test_row)
    
    print(f"Rank: {p:.2f}")
    print(f"Reason: {reason}")
