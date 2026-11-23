import csv
import random
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def choose(header, rows, label):
    """
    Finds the best working arrangement for 'Laboratory Technician' staff 
    by sampling up to 50 rows, labeling them, and using a Random Forest 
    to predict the best row among the lab staff.
    """
    goal_col = next(c for c in header if c.endswith('+') or c.endswith('-'))
    goal_idx = header.index(goal_col)
    role_idx = header.index('jobRole')
    is_maximize = goal_col.endswith('+')
    
    # Filter for Laboratory Technician indices
    lab_indices = [i for i, row in enumerate(rows) if row[role_idx] == 'Laboratory Technician']
    
    if not lab_indices:
        return 0
    
    # Sample up to 50 indices from the lab staff
    sample_size = min(50, len(lab_indices))
    indices_to_label = random.sample(lab_indices, sample_size)
    
    # Prepare training data
    train_rows = []
    for i in indices_to_label:
        row = list(rows[i])
        row[goal_idx] = label(i)[0]
        train_rows.append(row)
        
    df_train = pd.DataFrame(train_rows, columns=header)
    df_test = pd.DataFrame(rows, columns=header)
    
    # Separate features and target
    X = df_train.drop(columns=[goal_col])
    y = df_train[goal_col]
    X_test = df_test.drop(columns=[goal_col])
    
    # Encode symbolic columns
    for col in X.columns:
        if X[col].dtype == 'object':
            le = LabelEncoder()
            combined = pd.concat([X[col].astype(str), X_test[col].astype(str)], axis=0)
            le.fit(combined)
            X[col] = le.transform(X[col].astype(str))
            X_test[col] = le.transform(X_test[col].astype(str))
        else:
            X[col] = X[col].astype(float)
            X_test[col] = X_test[col].astype(float)
            
    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Predict for all lab staff
    predictions = model.predict(X_test)
    
    # Find the index with the best predicted value among lab staff
    if is_maximize:
        best_idx = max(lab_indices, key=lambda i: predictions[i])
    else:
        best_idx = min(lab_indices, key=lambda i: predictions[i])
        
    return best_idx

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed_row)
            
    goal_idx = next(i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-'))
    
    def label(i):
        return [rows[i][goal_idx]]
    
    masked_rows = []
    for row in rows:
        r = list(row)
        r[goal_idx] = "?"
        masked_rows.append(r)
        
    best_idx = choose(header, masked_rows, label)
    
    print(f"The best working arrangement for Laboratory Technicians found is at row index: {best_idx}")
    print(f"Goal column '{header[goal_idx]}' value: {rows[best_idx][goal_idx]}")
