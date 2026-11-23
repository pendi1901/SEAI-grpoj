import csv
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from step01 import remember as step01_remember

def find_similar(header, rows, target_row, n=5):
    """
    Finds the n most similar rows to target_row based on input columns.
    """
    df = pd.DataFrame(rows, columns=header)
    inputs = [c for c in header if not (c.endswith('-') or c.endswith('+'))]
    
    # Filter out rows that might have missing values (if any)
    # For this task, we assume input columns are fully populated
    X = df[inputs]
    
    # Use NearestNeighbors to find similarity
    nn = NearestNeighbors(n_neighbors=n)
    nn.fit(X)
    
    # Find neighbors for the target row (excluding goals)
    target_vals = [target_row[header.index(c)] for c in inputs]
    distances, indices = nn.kneighbors([target_vals])
    
    return indices[0]

def remember(header, rows):
    """
    Required function: returns indices of the best rows.
    """
    return step01_remember(header, rows)

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        # Pick a sample setup to simulate a customer proposal
        target_idx = 10
        target_row = rows[target_idx]
        
        # Find similar past setups
        similar_indices = find_similar(header, rows, target_row, n=3)
        
        print("Customer Inquiry: Show me past setups most like my proposal and their outcomes.")
        print(f"Target Proposal (Index {target_idx}):")
        print(f"  Inputs: {target_row[:len(header)-3]}")
        
        print("\nMost similar past setups:")
        goals = [c for c in header if c.endswith('-') or c.endswith('+')]
        for idx in similar_indices:
            outcome = {g: rows[idx][header.index(g)] for g in goals}
            print(f"  - Row {idx}: {outcome}")
            
        print("\nAnalysis: These historical records represent the closest configurations "
              "to your proposal. Comparing their outcomes helps predict the likely "
              "performance of your current setup.")
              
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
