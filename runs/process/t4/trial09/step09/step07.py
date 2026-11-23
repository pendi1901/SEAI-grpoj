import csv
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
from step01 import remember
from step02 import guess

def choose(header, rows, label):
    """
    Finds the best row by sampling 50 rows, using KNN to estimate 
    performance for the rest, and selecting the best overall.
    """
    # Identify input columns
    input_cols = [col for col in header if not (col.endswith('-') or col.endswith('+'))]
    goal_cols = [col for col in header if col.endswith(('-', '+'))]
    
    # 1. Sample 50 rows to build a training set
    # We pick indices spread across the dataset
    indices = np.linspace(0, len(rows) - 1, 50, dtype=int)
    
    train_rows = []
    train_goals = []
    
    for idx in indices:
        true_goals = label(idx)
        train_rows.append(rows[idx])
        train_goals.append(true_goals)
        
    # 2. Train a regressor to predict all goals
    # We use a simple MultiOutput approach via KNN
    model = KNeighborsRegressor(n_neighbors=3)
    model.fit([r[:len(input_cols)] for r in train_rows], train_goals)
    
    # 3. Predict goals for all rows
    all_inputs = [r[:len(input_cols)] for r in rows]
    all_preds = model.predict(all_inputs)
    
    # 4. Rank rows based on predicted aggregate score
    df_preds = pd.DataFrame(all_preds, columns=goal_cols)
    
    normalized_scores = []
    for goal in goal_cols:
        col_min = df_preds[goal].min()
        col_max = df_preds[goal].max()
        norm = (df_preds[goal] - col_min) / (col_max - col_min + 1e-9)
        if goal.endswith('-'):
            normalized_scores.append(1 - norm)
        else:
            normalized_scores.append(norm)
            
    aggregate = np.mean(normalized_scores, axis=0)
    
    # Return index of the best row
    return int(np.argmax(aggregate))

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            true_data = []
            for row in reader:
                numeric_row = [float(val) for val in row]
                rows.append(numeric_row)
                true_data.append(numeric_row[-3:]) # Last 3 are goals
        
        def label(i):
            return true_data[i]
            
        best_idx = choose(header, rows, label)
        
        print("Customer Inquiry: Best setup found after 50 trials.")
        print(f"The best configuration is at index: {best_idx}")
        print(f"Goal values for this setup: {true_data[best_idx]}")
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
