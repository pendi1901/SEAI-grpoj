import csv
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from step01 import remember as step01_remember

def find_similar(header, rows, target_row, n=5):
    """
    Finds the n most similar rows to the target_row based on input columns.
    """
    df = pd.DataFrame(rows, columns=header)
    inputs = [col for col in header if not (col.endswith('-') or col.endswith('+'))]
    
    # Filter rows that don't have '?' in input columns
    # (Assuming target_row is a complete input set for comparison)
    df_inputs = df[inputs]
    
    nn = NearestNeighbors(n_neighbors=n)
    nn.fit(df_inputs)
    
    # Find neighbors
    distances, indices = nn.kneighbors([target_row[:len(inputs)]])
    return indices[0]

def remember(header, rows):
    """
    Required by harness: returns indices of the best rows.
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
        
        # Example: Customer provides a setup (using the first row as a sample)
        target_setup = rows[0]
        
        # Find similar past setups
        similar_indices = find_similar(header, rows, target_setup)
        
        print("Customer Inquiry: Show me past setups most like my proposal and how they turned out.")
        print("-" * 60)
        
        goal_cols = [col for col in header if col.endswith(('-', '+'))]
        
        for idx in similar_indices:
            row = rows[idx]
            print(f"Setup Index {idx}:")
            for col in goal_cols:
                val = row[header.index(col)]
                print(f"  {col}: {val:.4f}")
            print("-" * 20)
            
        print("Conclusion: These are the most similar historical configurations found.")
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
