import csv
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from step01 import remember

def choose(header, rows, label):
    """
    Finds the best setup for a large, high-criticality project.
    We filter for rows where 'Size' and 'Criticality' are high,
    then use active learning to find the best among those.
    """
    # 1. Filter for large, high-criticality projects
    # We define "large" and "high-criticality" as being in the top 50%
    df = pd.DataFrame(rows, columns=header)
    size_thresh = df['Size'].median()
    crit_thresh = df['Criticality'].median()
    
    candidates = [i for i, row in enumerate(rows) 
                  if row[header.index('Size')] >= size_thresh 
                  and row[header.index('Criticality')] >= crit_thresh]
    
    # If no candidates, fall back to all rows
    if not candidates:
        candidates = list(range(len(rows)))
        
    # 2. Active Learning: Label up to 50 candidates
    goals = [col for col in header if col.endswith(('-', '+'))]
    inputs = [col for col in header if col not in goals]
    
    labeled_indices = []
    labeled_data = []
    
    # Initial sample: 20 from candidates
    sample_size = min(len(candidates), 20)
    indices_to_label = candidates[:sample_size]
    
    for i in indices_to_label:
        true_goals = label(i)
        row_data = rows[i][:]
        for j, goal in enumerate(goals):
            row_data[header.index(goal)] = true_goals[j]
        labeled_data.append(row_data)
        labeled_indices.append(i)
        
    # 3. Iterative search for remaining budget
    remaining_budget = 50 - len(labeled_indices)
    for _ in range(remaining_budget):
        if len(labeled_indices) >= len(candidates):
            break
            
        df_train = pd.DataFrame(labeled_data, columns=header)
        
        # Train models
        models = {}
        for goal in goals:
            m = RandomForestRegressor(n_estimators=20, random_state=42)
            m.fit(df_train[inputs], df_train[goal])
            models[goal] = m
            
        # Predict on remaining candidates
        unlabeled = [i for i in candidates if i not in labeled_indices]
        df_unlabeled = pd.DataFrame([rows[i] for i in unlabeled], columns=header)
        
        scores = pd.DataFrame(index=unlabeled)
        for goal in goals:
            pred = models[goal].predict(df_unlabeled[inputs])
            norm = (pred - pred.min()) / (pred.max() - pred.min() + 1e-9)
            scores[goal] = (1 - norm) if goal.endswith('-') else norm
            
        best_idx = scores.prod(axis=1).idxmax()
        
        # Label
        true_goals = label(best_idx)
        row_data = rows[best_idx][:]
        for j, goal in enumerate(goals):
            row_data[header.index(goal)] = true_goals[j]
        labeled_data.append(row_data)
        labeled_indices.append(best_idx)
        
    # 4. Return best from labeled
    best_in_labeled = remember(header, labeled_data)[0]
    return labeled_indices[best_in_labeled]

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) if val.replace('.','',1).isdigit() or (val.startswith('-') and val[1:].replace('.','',1).isdigit()) else val for val in row])
        
        true_goals_map = {i: [row[header.index(g)] for g in header if g.endswith(('-', '+'))] for i, row in enumerate(rows)}
        masked_rows = []
        for row in rows:
            m_row = row[:]
            for g in [c for c in header if c.endswith(('-', '+'))]:
                m_row[header.index(g)] = "?"
            masked_rows.append(m_row)
            
        best_idx = choose(header, masked_rows, lambda i: true_goals_map[i])
        print(f"Best setup for large, high-criticality project found at index: {best_idx}")
        print(f"Setup details: {rows[best_idx]}")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
