import csv
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from step01 import remember

def choose(header, rows, label):
    """
    Finds the best row by sampling 50 candidates using an acquisition function.
    """
    input_cols = [col for col in header if not (col.endswith('-') or col.endswith('+'))]
    goal_cols = [col for col in header if col.endswith(('-', '+'))]
    
    # Convert rows to DataFrame for easier handling
    df = pd.DataFrame(rows, columns=header)
    
    # 1. Initial exploration: Sample 10 random rows to build a baseline model
    indices = list(range(len(rows)))
    np.random.shuffle(indices)
    
    labeled_indices = []
    for i in indices[:10]:
        goals = label(i)
        for idx, col in enumerate(goal_cols):
            df.at[i, col] = goals[idx]
        labeled_indices.append(i)
        
    # 2. Active learning: Sample remaining 40 rows
    # We use a Random Forest to predict the aggregate score and pick the best
    for _ in range(40):
        # Train model on currently labeled data
        train_df = df.loc[labeled_indices]
        X = train_df[input_cols]
        
        # Calculate aggregate score for labeled data
        scores = pd.DataFrame(index=train_df.index)
        for goal in goal_cols:
            col_data = train_df[goal]
            norm = (col_data - col_data.min()) / (col_data.max() - col_data.min() + 1e-9)
            scores[goal] = (1 - norm) if goal.endswith('-') else norm
        y = scores.mean(axis=1)
        
        model = RandomForestRegressor(n_estimators=20, random_state=42)
        model.fit(X, y)
        
        # Predict scores for all unlabeled rows
        unlabeled = [i for i in range(len(rows)) if i not in labeled_indices]
        X_unlabeled = df.loc[unlabeled, input_cols]
        preds = model.predict(X_unlabeled)
        
        # Pick the best predicted row
        best_unlabeled_idx = unlabeled[np.argmax(preds)]
        
        # Label it
        goals = label(best_unlabeled_idx)
        for idx, col in enumerate(goal_cols):
            df.at[best_unlabeled_idx, col] = goals[idx]
        labeled_indices.append(best_unlabeled_idx)
        
    # 3. Return the index of the best row found
    final_scores = pd.DataFrame(index=labeled_indices)
    for goal in goal_cols:
        col_data = df.loc[labeled_indices, goal]
        norm = (col_data - col_data.min()) / (col_data.max() - col_data.min() + 1e-9)
        final_scores[goal] = (1 - norm) if goal.endswith('-') else norm
    
    best_idx = final_scores.mean(axis=1).idxmax()
    return int(best_idx)

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row[:9]] + ["?"] * 3)
        
        # Mock label function for standalone execution
        full_data = pd.read_csv(filename).values.tolist()
        def label(i):
            return full_data[i][9:]
            
        best_idx = choose(header, rows, label)
        print(f"The best row found after 50 trials is at index: {best_idx}")
        exit(0)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
