import csv
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from step01 import remember as get_best_indices

def remember(header, rows):
    """
    Returns the indices of the top 5% of rows based on aggregate goal performance.
    Required by the test harness.
    """
    return get_best_indices(header, rows)

def find_similar(header, rows, target_row):
    """
    Finds the 5 most similar historical rows to the target_row 
    using Euclidean distance on input columns.
    """
    df = pd.DataFrame(rows, columns=header)
    input_cols = [col for col in header if not (col.endswith('-') or col.endswith('+'))]
    
    # Focus on inputs
    X = df[input_cols]
    
    # Use KNN to find neighbors
    nn = NearestNeighbors(n_neighbors=5)
    nn.fit(X)
    
    # Find neighbors for the target row
    target_df = pd.DataFrame([target_row], columns=header)[input_cols]
    distances, indices = nn.kneighbors(target_df)
    
    return indices[0].tolist()

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        df = pd.read_csv(filename)
        header = df.columns.tolist()
        rows = df.values.tolist()
        
        # The customer asks to see past setups most like their proposal
        # We simulate a proposal using the first row's inputs
        proposal = rows[0][:9] + ["?"] * 3
        
        # Find similar past setups
        similar_indices = find_similar(header, rows, proposal)
        
        print("Proposed setup is similar to these historical rows:")
        goal_cols = [col for col in header if col.endswith(('-', '+'))]
        for idx in similar_indices:
            row = rows[idx]
            goals = {col: row[header.index(col)] for col in goal_cols}
            goal_str = ", ".join([f"{k}: {v:.3f}" for k, v in goals.items()])
            print(f"Row {idx} -> {goal_str}")
            
        # Identify if any of these are actually "best"
        best_indices = remember(header, rows)
        overlap = set(similar_indices) & set(best_indices)
        if overlap:
            print(f"\nNote: Some of these similar setups are among our top-performing configurations: {list(overlap)}")
        else:
            print("\nNote: These similar setups are not among our top-performing configurations.")
            
        exit(0)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
