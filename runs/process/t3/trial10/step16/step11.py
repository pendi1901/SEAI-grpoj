import csv
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

def remember(header, rows):
    """
    Identifies the best rows by calculating a normalized score for each row
    and returning the indices of the top 5% of performers.
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Identify goal columns
    goal_cols = [col for col in header if col.endswith(('-', '+'))]
    
    # Normalize goals to [0, 1] range
    # For '-', lower is better (1 - normalized value)
    # For '+', higher is better (normalized value)
    scores = []
    for col in goal_cols:
        col_min = df[col].min()
        col_max = df[col].max()
        # Avoid division by zero
        rng = col_max - col_min
        if rng == 0:
            norm = 0
        else:
            norm = (df[col] - col_min) / rng
            
        if col.endswith('-'):
            scores.append(1 - norm)
        else:
            scores.append(norm)
            
    # Aggregate score: mean of normalized goals
    combined_score = np.mean(scores, axis=0)
    
    # Select top 5% of rows
    num_to_select = max(1, len(rows) // 20)
    top_indices = np.argsort(combined_score)[-num_to_select:]
    
    return sorted(top_indices.tolist())

def find_similar(header, rows, target_row, n=3):
    """
    Finds the n most similar rows to the target_row using Euclidean distance
    on input columns.
    """
    input_cols = [col for col in header if not (col.endswith('-') or col.endswith('+'))]
    df = pd.DataFrame(rows, columns=header)
    
    # Extract input data
    X = df[input_cols].values
    target_vals = np.array([target_row[i] for i, col in enumerate(header) if col in input_cols]).reshape(1, -1)
    
    # Find nearest neighbors
    nn = NearestNeighbors(n_neighbors=n)
    nn.fit(X)
    distances, indices = nn.kneighbors(target_vals)
    
    return indices[0]

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        # Example: The customer proposes the first row as their setup
        target_row = rows[0]
        
        # 1. Get the best setups
        best_indices = remember(header, rows)
        
        # 2. Find setups similar to the proposed one
        similar_indices = find_similar(header, rows, target_row)
        
        print("Customer Inquiry: Setup Analysis")
        print(f"Your proposed setup is similar to the following historical configurations:")
        
        goal_cols = [col for col in header if col.endswith(('-', '+'))]
        for idx in similar_indices:
            goals = [f"{col}: {rows[idx][header.index(col)]:.4f}" for col in goal_cols]
            print(f"- Index {idx}: {', '.join(goals)}")
            
        print(f"\nFor reference, the top-performing setups in our database are at indices:")
        print(best_indices[:10])
        
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)
