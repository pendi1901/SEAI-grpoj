import csv
import pandas as pd
import numpy as np
from step01 import remember
from step02 import guess

def choose(header, rows, label):
    """
    Finds the best row by sampling 50 setups.
    We use a simple strategy: sample 50 rows, label them, 
    and pick the one with the best aggregate score.
    """
    # Identify indices
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    
    # We can label at most 50 rows. 
    # Let's pick 50 indices spread across the dataset.
    num_rows = len(rows)
    indices_to_sample = np.linspace(0, num_rows - 1, 50, dtype=int)
    
    best_idx = -1
    best_score = float('inf')
    
    # Store labeled data to normalize
    labeled_data = []
    
    for i in indices_to_sample:
        goals = label(i)
        labeled_data.append((i, goals))
        
    # Normalize goals to calculate aggregate score
    df_goals = pd.DataFrame([x[1] for x in labeled_data])
    normalized = (df_goals - df_goals.min()) / (df_goals.max() - df_goals.min())
    
    # Calculate scores
    goal_types = ['min' if header[idx].endswith('-') else 'max' for idx in goal_indices]
    
    for i, (orig_idx, goals) in enumerate(labeled_data):
        score = 0
        for j, g_type in enumerate(goal_types):
            val = normalized.iloc[i, j]
            score += val if g_type == 'min' else (1 - val)
            
        if score < best_score:
            best_score = score
            best_idx = orig_idx
            
    return int(best_idx)

if __name__ == "__main__":
    filename = 'pom3a.train.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)
    
    # Keep true goals for the label function
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    true_goals = [[float(row[i]) for i in goal_indices] for row in rows]
    
    def label(i):
        return true_goals[i]
    
    best_row_idx = choose(header, rows, label)
    
    print("Customer Inquiry: I can afford to trial 50 setups for real. Find me the best one.")
    print(f"Analysis complete. The best setup found is at index {best_row_idx}.")
    print(f"True goal values for this setup: {true_goals[best_row_idx]}")
