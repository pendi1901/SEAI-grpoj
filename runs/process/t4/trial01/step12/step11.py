import csv
from sklearn.neighbors import NearestNeighbors

def remember(header, rows):
    """
    Finds the most similar past configurations to the proposed setup (the last row).
    Returns the indices of the most similar rows.
    """
    # Identify input columns (non-goal columns)
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    input_indices = [i for i in range(len(header)) if i not in goal_indices]
    
    # The last row is the proposal
    proposal = rows[-1]
    past_rows = rows[:-1]
    
    # Prepare data for similarity search
    X = [[row[i] for i in input_indices] for row in past_rows]
    query = [[proposal[i] for i in input_indices]]
    
    # Find 5 most similar rows
    nn = NearestNeighbors(n_neighbors=5)
    nn.fit(X)
    distances, indices = nn.kneighbors(query)
    
    return indices[0].tolist()

def get_performance(header, row):
    """Summarizes how a row turned out."""
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    summary = []
    for idx in goal_indices:
        summary.append(f"{header[idx]}: {row[idx]:.3f}")
    return ", ".join(summary)

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        # We assume the last row is the user's proposal
        proposal = rows[-1]
        similar_indices = remember(header, rows)
        
        print("The proposed setup is most similar to these past configurations:")
        for idx in similar_indices:
            print(f"Row {idx}: {get_performance(header, rows[idx])}")
            
        exit(0)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
