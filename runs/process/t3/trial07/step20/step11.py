import csv
import pandas as pd
from sklearn.neighbors import NearestNeighbors

def remember(header, rows):
    """
    Finds the 5% of rows that are most similar to the 'best' performing rows
    in the dataset, based on input parameters.
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Identify goal and input columns
    goal_cols = [col for col in header if col.endswith(('-', '+'))]
    input_cols = [col for col in header if col not in goal_cols]
    
    # Normalize goals to find the 'best' rows
    scores = pd.DataFrame(index=df.index)
    for goal in goal_cols:
        col_data = df[goal].astype(float)
        norm = (col_data - col_data.min()) / (col_data.max() - col_data.min() + 1e-9)
        scores[goal] = 1 - norm if goal.endswith('-') else norm
    
    df['aggregate'] = scores.mean(axis=1)
    
    # Find top 5% of rows based on performance
    n_rows = len(df)
    k = max(1, int(n_rows * 0.05))
    best_performers = df.nlargest(k, 'aggregate')
    
    # Use KNN to find rows in the dataset most similar to these top performers
    # based on input features
    nn = NearestNeighbors(n_neighbors=k)
    nn.fit(df[input_cols])
    
    # Find the k nearest neighbors to the best performers
    distances, indices = nn.kneighbors(best_performers[input_cols])
    
    # Flatten indices and return unique ones
    result_indices = sorted(list(set(indices.flatten())))
    
    # Ensure we return exactly k indices if possible, or at least 1
    return result_indices[:k]

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        best_indices = remember(header, rows)
        
        print("Customer Inquiry: Show me the past setups most like the best ones.")
        print(f"Analysis: Identified {len(best_indices)} configurations that are most similar to our top performers.")
        print("Indices of these configurations:")
        print(best_indices)
        
        # Summary of the first one
        first_idx = best_indices[0]
        print(f"\nExample of a top-tier configuration (Index {first_idx}):")
        for h, v in zip(header, rows[first_idx]):
            print(f"  {h}: {v:.4f}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
