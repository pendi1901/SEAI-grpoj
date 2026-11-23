import csv
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from step01 import remember as step01_remember

def remember(header, rows):
    """
    Returns the indices of the best rows as per the logic in step01.
    """
    return step01_remember(header, rows)

def find_similar(header, rows, target_row, n=5):
    """
    Finds the n most similar rows to the target_row based on input columns.
    """
    df = pd.DataFrame(rows, columns=header)
    inputs = [col for col in header if not (col.endswith(('-', '+')))]
    
    # Use KNN to find nearest neighbors in input space
    nn = NearestNeighbors(n_neighbors=n)
    nn.fit(df[inputs])
    
    # Extract inputs from target_row
    target_inputs = [target_row[header.index(col)] for col in inputs]
    
    distances, indices = nn.kneighbors([target_inputs])
    return indices[0]

def explain_outcomes(header, rows, indices):
    """
    Summarizes the outcomes of the provided row indices.
    """
    goals = [col for col in header if col.endswith(('-', '+'))]
    results = []
    for idx in indices:
        row = rows[idx]
        outcome = {goal: row[header.index(goal)] for goal in goals}
        results.append(outcome)
    return results

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        # Customer's proposed setup (using the first row as an example)
        proposed_setup = rows[0]
        
        # Find 5 most similar past setups
        similar_indices = find_similar(header, rows, proposed_setup, n=5)
        outcomes = explain_outcomes(header, rows, similar_indices)
        
        print("Customer Inquiry: Show me past setups most like mine and how they turned out.")
        print(f"Found {len(similar_indices)} similar historical setups:")
        for i, (idx, outcome) in enumerate(zip(similar_indices, outcomes), 1):
            print(f"\nSetup {i} (Index {idx}):")
            for goal, val in outcome.items():
                print(f"  {goal}: {val:.4f}")
                
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
