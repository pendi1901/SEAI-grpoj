import csv
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def choose(header, rows, label):
    """
    Finds the best setup by sampling 50 rows, using a Random Forest to 
    predict performance, and selecting the best predicted configuration.
    """
    n_rows = len(rows)
    input_cols = [c for c in header if not (c.endswith('-') or c.endswith('+'))]
    goal_cols = [c for c in header if c.endswith('-') or c.endswith('+')]
    
    # 1. Sample 50 indices to label
    # We pick a mix of random and spread out indices
    indices_to_label = np.linspace(0, n_rows - 1, 50, dtype=int)
    
    train_X = []
    train_y = []
    
    # 2. Label the sampled rows
    for i in indices_to_label:
        goals = label(i)
        # Normalize goals to a single score [0, 1]
        # We need to estimate global min/max for normalization
        # Since we don't have them, we use the sampled goals as a proxy
        train_X.append([rows[i][header.index(c)] for c in input_cols])
        train_y.append(goals)
        
    train_y = np.array(train_y)
    
    # Normalize goals for the score
    norm_y = np.zeros_like(train_y, dtype=float)
    for j, col in enumerate(goal_cols):
        c_min, c_max = train_y[:, j].min(), train_y[:, j].max()
        if c_max == c_min:
            norm_y[:, j] = 0.5
        elif col.endswith('-'):
            norm_y[:, j] = (c_max - train_y[:, j]) / (c_max - c_min)
        else:
            norm_y[:, j] = (train_y[:, j] - c_min) / (c_max - c_min)
    
    scores = norm_y.mean(axis=1)
    
    # 3. Train a model to predict the score
    df_X = pd.DataFrame(train_X, columns=input_cols)
    for col in input_cols:
        if df_X[col].dtype == 'object':
            le = LabelEncoder()
            df_X[col] = le.fit_transform(df_X[col].astype(str))
            
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(df_X, scores)
    
    # 4. Predict scores for all rows
    all_X = pd.DataFrame(rows, columns=header)[input_cols]
    for col in input_cols:
        if all_X[col].dtype == 'object':
            le = LabelEncoder()
            all_X[col] = le.fit_transform(all_X[col].astype(str))
            
    all_scores = model.predict(all_X)
    
    # 5. Return index of the best predicted row
    return int(np.argmax(all_scores))

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.train.csv'
    data = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for val in row:
                try:
                    processed_row.append(float(val))
                except ValueError:
                    processed_row.append(val)
            data.append(processed_row)
            
    # Keep true goals for the label function
    true_data = [row[:] for row in data]
    # Mask goals in the rows passed to choose
    masked_data = []
    for row in data:
        new_row = [("?" if (header[i].endswith('-') or header[i].endswith('+')) else row[i]) 
                   for i in range(len(row))]
        masked_data.append(new_row)
        
    def label(i):
        return [true_data[i][j] for j, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
        
    best_idx = choose(header, masked_data, label)
    print(f"The best setup found is at index {best_idx}.")
