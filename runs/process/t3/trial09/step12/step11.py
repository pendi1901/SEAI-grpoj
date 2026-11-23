import csv
import pandas as pd
from sklearn.neighbors import NearestNeighbors

def remember(header, rows):
    """
    Identifies the best rows based on goal optimization.
    Returns the indices of the top 5% of rows.
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Identify goal columns
    goals = [c for c in header if c.endswith('-') or c.endswith('+')]
    
    # Normalize goals to [0, 1] range
    # For '-', lower is better (1 - normalized_val)
    # For '+', higher is better (normalized_val)
    normalized_goals = pd.DataFrame(index=df.index)
    for goal in goals:
        col = df[goal].astype(float)
        norm = (col - col.min()) / (col.max() - col.min() + 1e-9)
        if goal.endswith('-'):
            normalized_goals[goal] = 1 - norm
        else:
            normalized_goals[goal] = norm
            
    # Calculate a score: the mean of normalized goals
    scores = normalized_goals.mean(axis=1)
    
    # Select top 5%
    n_select = max(1, int(len(rows) * 0.05))
    best_indices = scores.nlargest(n_select).index.tolist()
    
    return sorted(best_indices)

def find_similar_and_outcomes(header, rows, target_row, n_neighbors=3):
    """
    Finds the most similar past rows to the target_row and reports their outcomes.
    """
    df = pd.DataFrame(rows, columns=header)
    goals = [c for c in header if c.endswith('-') or c.endswith('+')]
    inputs = [c for c in header if c not in goals]
    
    # Use KNN to find similar rows based on input features
    nn = NearestNeighbors(n_neighbors=n_neighbors)
    nn.fit(df[inputs])
    
    distances, indices = nn.kneighbors([target_row[:len(inputs)]])
    
    results = []
    for idx in indices[0]:
        row_data = df.iloc[idx]
        outcomes = {g: row_data[g] for g in goals}
        results.append((idx, outcomes))
    return results

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) if i < len(header) - 3 or (i >= len(header) - 3 and val.replace('.','',1).isdigit()) else val for i, val in enumerate(row)])
        
        # Example: User proposes a setup (using the first row as a sample)
        target_row = rows[0]
        
        print("Customer Inquiry: Show me past setups most like mine and their outcomes.")
        print("-" * 60)
        
        similar = find_similar_and_outcomes(header, rows, target_row)
        
        for idx, outcomes in similar:
            print(f"Found similar setup at index {idx}:")
            for goal, val in outcomes.items():
                print(f"  {goal}: {val:.4f}")
            print("-" * 20)
            
        # Also identify the best overall setups as requested by the harness
        best_indices = remember(header, rows)
        print(f"\nFor reference, the top-performing setups in our database are at indices: {best_indices[:5]}...")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
