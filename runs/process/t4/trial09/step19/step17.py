import csv
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor

def choose(header, rows, label):
    """
    Finds the best setup for a large project by sampling 50 rows,
    using KNN to predict performance, and selecting the best.
    """
    input_cols = [i for i, h in enumerate(header) if not (h.endswith('-') or h.endswith('+'))]
    goal_cols = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
    
    # 1. Sample 50 rows to build a training set
    # We pick indices spread across the dataset to get a good representation
    indices = np.linspace(0, len(rows) - 1, 50, dtype=int)
    
    train_inputs = []
    train_goals = []
    
    for idx in indices:
        true_goals = label(idx)
        train_inputs.append([rows[idx][c] for c in input_cols])
        train_goals.append(true_goals)
        
    # 2. Train a regressor to predict all goals
    model = KNeighborsRegressor(n_neighbors=3)
    model.fit(train_inputs, train_goals)
    
    # 3. Predict goals for all rows
    all_inputs = [[rows[i][c] for c in input_cols] for i in range(len(rows))]
    all_preds = model.predict(all_inputs)
    
    # 4. Rank rows based on predicted aggregate score
    df_preds = pd.DataFrame(all_preds, columns=goal_cols)
    
    normalized_scores = []
    for i, goal in enumerate(goal_cols):
        col_min = df_preds[goal].min()
        col_max = df_preds[goal].max()
        norm = (df_preds[goal] - col_min) / (col_max - col_min + 1e-9)
        if header[goal].endswith('-'):
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
            true_goals = []
            for row in reader:
                numeric_row = [float(val) for val in row]
                rows.append(numeric_row)
                true_goals.append(numeric_row[-3:]) # Last 3 are goals
        
        def label(i):
            return true_goals[i]
            
        best_idx = choose(header, rows, label)
        
        print("Customer Inquiry: Best setup for a large, high-stakes project.")
        print(f"Analysis: After trialling 50 configurations, the best setup is at index {best_idx}.")
        print(f"Goal values for this setup: {true_goals[best_idx]}")
        print("Conclusion: This configuration provides the most optimal balance of cost and performance.")
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
