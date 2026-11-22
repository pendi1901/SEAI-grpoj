import csv
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

def remember(header, rows):
    """
    Identifies the 5% of rows that perform best across all goal columns.
    Goals ending in '-' are minimized, '+' are maximized.
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Identify goal columns
    goals = [c for c in header if c.endswith('-') or c.endswith('+')]
    
    # Normalize goals to [0, 1] range to treat them equally
    # For '-', lower is better (1 - normalized_val)
    # For '+', higher is better (normalized_val)
    scores = []
    for col in goals:
        vals = df[col].astype(float)
        norm = (vals - vals.min()) / (vals.max() - vals.min() + 1e-9)
        if col.endswith('-'):
            scores.append(1 - norm)
        else:
            scores.append(norm)
            
    # Aggregate scores (mean of normalized goals)
    df['aggregate'] = np.mean(scores, axis=0)
    
    # Select top 5% (or at least 1)
    n_rows = len(rows)
    k = max(1, n_rows // 20)
    
    top_indices = df['aggregate'].nlargest(k).index.tolist()
    return top_indices

def find_similar(header, rows, target_row, n=3):
    """
    Finds the n most similar rows to the target_row based on input columns.
    """
    df = pd.DataFrame(rows, columns=header)
    goals = [c for c in header if c.endswith('-') or c.endswith('+')]
    inputs = [c for c in header if c not in goals]
    
    # Prepare input data for similarity search
    X = df[inputs]
    target_vals = [target_row[header.index(c)] for c in inputs]
    
    # Use KNN to find nearest neighbors
    nn = NearestNeighbors(n_neighbors=n)
    nn.fit(X)
    distances, indices = nn.kneighbors([target_vals])
    
    return indices[0].tolist()

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) if val.replace('.', '', 1).isdigit() or 
                             (val.startswith('-') and val[1:].replace('.', '', 1).isdigit()) 
                             else val for val in row])
        
        # Example: Customer provides a setup (using the first row as an example)
        target_row = rows[0]
        
        # Find similar past setups
        similar_indices = find_similar(header, rows, target_row)
        
        print("Customer Inquiry: Show me past setups similar to my proposal.")
        print("-" * 60)
        for idx in similar_indices:
            row = rows[idx]
            goals = {c: row[header.index(c)] for c in header if c.endswith('-') or c.endswith('+')}
            print(f"Setup at index {idx}:")
            print(f"  Goals: {goals}")
        
        print("-" * 60)
        print("These past configurations are the most similar in terms of input parameters.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
