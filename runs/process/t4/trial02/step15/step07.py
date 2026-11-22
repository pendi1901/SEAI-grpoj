import csv
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from step01 import remember

def choose(header, rows, label):
    """
    Finds the best row by using an active learning approach:
    1. Use a surrogate model (Random Forest) to predict goals.
    2. Use Expected Improvement or simply pick the best predicted row.
    3. Label the best candidates until 50 are used.
    """
    goals = [c for c in header if c.endswith('-') or c.endswith('+')]
    inputs = [c for c in header if c not in goals]
    
    # Track which rows have been labeled
    labeled_indices = {}
    
    # Initial strategy: sample 10 rows randomly to seed the model
    initial_samples = np.random.choice(len(rows), min(10, len(rows)), replace=False)
    for idx in initial_samples:
        labeled_indices[idx] = label(idx)
        
    # Iteratively improve
    for _ in range(50 - len(labeled_indices)):
        # Train model on currently labeled data
        train_x = [rows[i][:-len(goals)] for i in labeled_indices]
        train_y = [labeled_indices[i] for i in labeled_indices]
        
        # Predict goals for all unlabeled rows
        unlabeled_indices = [i for i in range(len(rows)) if i not in labeled_indices]
        if not unlabeled_indices:
            break
            
        # Use RF to predict each goal
        preds = []
        for g_idx in range(len(goals)):
            rf = RandomForestRegressor(n_estimators=20)
            rf.fit(train_x, [y[g_idx] for y in train_y])
            preds.append(rf.predict([rows[i][:-len(goals)] for i in unlabeled_indices]))
        
        # Evaluate predicted performance
        # Create a temporary list of rows with predicted goals
        temp_rows = []
        for i, u_idx in enumerate(unlabeled_indices):
            row_vals = rows[u_idx][:-len(goals)] + [preds[g_idx][i] for g_idx in range(len(goals))]
            temp_rows.append(row_vals)
            
        # Use remember logic to find the best predicted row
        best_in_temp = remember(header, temp_rows)[0]
        best_idx = unlabeled_indices[best_in_temp]
        
        # Label it
        labeled_indices[best_idx] = label(best_idx)
        
    # Final selection: find the best among all labeled rows
    final_data = []
    indices = []
    for idx, vals in labeled_indices.items():
        final_data.append(rows[idx][:-len(goals)] + vals)
        indices.append(idx)
        
    best_local_idx = remember(header, final_data)[0]
    return indices[best_local_idx]

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            full_rows = []
            for row in reader:
                full_rows.append([float(val) for val in row])
        
        # Setup hidden rows
        goals = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
        rows = []
        true_goals = []
        for r in full_rows:
            row_copy = r[:]
            true_goals.append([r[g] for g in goals])
            for g in goals:
                row_copy[g] = "?"
            rows.append(row_copy)
            
        def label(i):
            return true_goals[i]
            
        best_idx = choose(header, rows, label)
        print(f"Best row found at index: {best_idx}")
        print("The setup has been identified using an active learning strategy over 50 trials.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
