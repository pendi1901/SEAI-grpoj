import csv
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsRegressor

def justify(header, rows, row):
    """
    Estimates the goal values for the provided row using KNN, then calculates
    the percentile rank of this row against the existing dataset.
    """
    df = pd.DataFrame(rows, columns=header)
    input_cols = [col for col in header if not (col.endswith('-') or col.endswith('+'))]
    goal_cols = [col for col in header if col.endswith(('-', '+'))]
    
    # 1. Estimate goals for the target row using KNN
    X_train = df[input_cols]
    y_train = df[goal_cols]
    model = KNeighborsRegressor(n_neighbors=10)
    model.fit(X_train, y_train)
    
    # Create a DataFrame for the single row to predict
    # Fill "?" with the mean of the column for prediction purposes
    row_filled = []
    for i, val in enumerate(row):
        if val == "?":
            row_filled.append(df[header[i]].mean())
        else:
            row_filled.append(val)
            
    row_df = pd.DataFrame([row_filled], columns=header)
    predicted_goals = model.predict(row_df[input_cols])[0]
    
    # 2. Calculate scores for all rows (normalized 0 to 1)
    # For '-', lower is better; for '+', higher is better.
    def get_normalized_score(data_frame):
        scores = []
        for col in goal_cols:
            col_min = df[col].min()
            col_max = df[col].max()
            norm = (data_frame[col] - col_min) / (col_max - col_min + 1e-9)
            scores.append(1 - norm if col.endswith('-') else norm)
        return np.mean(scores, axis=1)

    all_scores = get_normalized_score(df)
    
    # 3. Calculate score for the target row
    norm_target = []
    for i, col in enumerate(goal_cols):
        col_min = df[col].min()
        col_max = df[col].max()
        val = predicted_goals[i]
        norm = (val - col_min) / (col_max - col_min + 1e-9)
        norm_target.append(1 - norm if col.endswith('-') else norm)
    
    target_score = np.mean(norm_target)
    
    # 4. Calculate percentile (fraction of rows that are worse)
    p = float(np.mean(all_scores < target_score))
    
    reason = f"This setup is estimated to outperform {p:.2f} of all known project configurations based on its projected efficiency across all primary goals."
    
    return p, reason

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        # Example: Compare a hypothetical setup B (index 1) against the dataset
        test_row = rows[1][:]
        goal_indices = [i for i, col in enumerate(header) if col.endswith(('-', '+'))]
        for idx in goal_indices:
            test_row[idx] = "?"
            
        p, reason = justify(header, rows, test_row)
        print(f"Justification Result:")
        print(f"Percentile: {p:.4f}")
        print(f"Reason: {reason}")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)
