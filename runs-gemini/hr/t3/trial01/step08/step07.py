import pandas as pd
import numpy as np

def choose(header, rows, label):
    """
    Finds the best working arrangement by sampling 50 rows.
    We use a simple strategy: sample 50 random rows, query their true goals,
    and identify the one with the highest composite score.
    """
    goal_cols = [i for i, c in enumerate(header) if c.endswith('+') or c.endswith('-')]
    
    # Randomly select 50 indices to label
    np.random.seed(42)
    indices_to_sample = np.random.choice(len(rows), size=min(50, len(rows)), replace=False)
    
    best_idx = -1
    best_score = -float('inf')
    
    # We need to normalize goals to compare them. 
    # Since we only have 50 samples, we use the min/max of the sampled data.
    sampled_data = []
    for idx in indices_to_sample:
        goals = label(idx)
        sampled_data.append(goals)
    
    sampled_goals = np.array(sampled_data)
    
    # Normalize: for '+', higher is better; for '-', lower is better.
    # We'll use (val - min) / (max - min) for '+' and (max - val) / (max - min) for '-'
    normalized_scores = np.zeros(sampled_goals.shape)
    for i, col_idx in enumerate(goal_cols):
        col_name = header[col_idx]
        col_vals = sampled_goals[:, i]
        col_min, col_max = col_vals.min(), col_vals.max()
        diff = col_max - col_min if col_max != col_min else 1.0
        
        if col_name.endswith('+'):
            normalized_scores[:, i] = (col_vals - col_min) / diff
        else:
            normalized_scores[:, i] = (col_max - col_vals) / diff
            
    # Calculate composite score (sum of normalized goals)
    total_scores = normalized_scores.sum(axis=1)
    
    # Find the index of the best row
    best_pos = np.argmax(total_scores)
    return indices_to_sample[best_pos]

if __name__ == "__main__":
    df = pd.read_csv('WA_Fn-UseC_-HR-Employee-Attrition.train.csv')
    header = df.columns.tolist()
    rows = df.values.tolist()
    
    # Define the label function for the test harness
    goal_indices = [i for i, c in enumerate(header) if c.endswith('+') or c.endswith('-')]
    
    def label(i):
        return [float(rows[i][idx]) for idx in goal_indices]
    
    # Mask the rows
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    best_idx = choose(header, masked_rows, label)
    
    print("Analysis complete.")
    print(f"The best working arrangement found among the 50 sampled staff is at row index {best_idx}.")
    print("This row was identified by maximizing the composite score of tenure-related goals.")
    exit(0)
