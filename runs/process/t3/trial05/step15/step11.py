import csv
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

def remember(header, rows):
    """
    Identifies the rows most similar to the proposed setup (the first row)
    and returns the indices of the best-performing ones among those neighbors.
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Identify input columns (those not ending in - or +)
    input_cols = [c for c in header if not (c.endswith('-') or c.endswith('+'))]
    goal_cols = [c for c in header if c.endswith('-') or c.endswith('+')]
    
    # Normalize goals to a [0, 1] scale where 1 is "best"
    scores = pd.DataFrame(index=df.index)
    for goal in goal_cols:
        col = df[goal].astype(float)
        if goal.endswith('-'):
            scores[goal] = (col.max() - col) / (col.max() - col.min() + 1e-9)
        else:
            scores[goal] = (col - col.min()) / (col.max() - col.min() + 1e-9)
    
    df['composite'] = scores.mean(axis=1)
    
    # Find 20 nearest neighbors to the proposed setup (index 0)
    nn = NearestNeighbors(n_neighbors=20)
    nn.fit(df[input_cols])
    distances, indices = nn.kneighbors([df.iloc[0][input_cols]])
    
    # From these neighbors, return the indices of the best performers
    neighbor_df = df.iloc[indices[0]]
    k = max(1, int(len(rows) * 0.05))
    best_indices = neighbor_df.nlargest(k, 'composite').index.tolist()
    
    return sorted(best_indices)

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        indices = remember(header, rows)
        
        print("Customer Inquiry: Show me past setups most like my proposal and how they turned out.")
        print(f"Analysis: Found {len(indices)} similar historical setups that performed well.")
        print("Indices of the most similar high-performing setups:")
        print(indices)
        
        # Summary of the first similar setup
        best_idx = indices[0]
        print(f"\nExample of a similar high-performing setup (index {best_idx}):")
        for h, v in zip(header, rows[best_idx]):
            print(f"  {h}: {v:.4f}")
            
        exit(0)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
