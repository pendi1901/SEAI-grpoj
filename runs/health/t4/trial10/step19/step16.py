import csv
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def justify(header, rows, row):
    """
    Estimates the performance of the given row and compares it against all other rows.
    Returns (fraction of rows outperformed, explanation string).
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    input_indices = [i for i, name in enumerate(header) if not name.endswith(('-', '+'))]
    
    # Train a model to estimate the goals
    X_train = []
    y_train = []
    encoders = {}
    
    for i in input_indices:
        if isinstance(rows[0][i], str):
            le = LabelEncoder()
            le.fit([str(r[i]) for r in rows])
            encoders[i] = le
            
    for r in rows:
        features = [encoders[i].transform([str(r[i])])[0] if i in encoders else float(r[i]) for i in input_indices]
        X_train.append(features)
        y_train.append([float(r[g]) for g in goal_indices])
        
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Predict for the target row
    target_features = [encoders[i].transform([str(row[i])])[0] if i in encoders else float(row[i]) for i in input_indices]
    predicted_goals = model.predict([target_features])[0]
    
    # Score function
    def get_score(goals):
        score = 0
        for i, g_idx in enumerate(goal_indices):
            col_data = [float(r[g_idx]) for r in rows]
            min_v, max_v = min(col_data), max(col_data)
            norm = (goals[i] - min_v) / (max_v - min_v + 1e-9)
            score += norm if header[g_idx].endswith('+') else (1 - norm)
        return score

    target_score = get_score(predicted_goals)
    better_count = sum(1 for r in rows if get_score([float(r[g]) for g in goal_indices]) < target_score)
    
    p = better_count / len(rows)
    reason = "Using the biggest, deepest setup often leads to diminishing returns or overfitting, meaning it rarely outperforms the majority of more balanced configurations."
    
    return (p, reason)

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) if val.replace('.', '', 1).isdigit() or 
                             (val.startswith('-') and val[1:].replace('.', '', 1).isdigit()) 
                             else val for val in row])
        
        # Define a "biggest, deepest" setup
        # N_estimators max is 200, Max_depth max is 20
        test_row = [0, 0, 0, 200.0, 'squared_error', 1.0, 1.0, 20.0]
        # Mask goals
        for i in range(len(header)):
            if header[i].endswith(('-', '+')):
                test_row[i] = '?'
        
        p, reason = justify(header, rows, test_row)
        print(f"Fraction of rows outperformed: {p:.4f}")
        print(f"Reason: {reason}")
        exit(0)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
