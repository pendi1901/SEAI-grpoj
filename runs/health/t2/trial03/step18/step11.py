import csv
from step01 import remember as base_remember

def find_similar(header, rows, target_row, n=5):
    """
    Finds the n rows most similar to the target_row based on input features.
    """
    input_indices = [i for i, name in enumerate(header) if name not in ['MRE-', 'ACC+', 'PRED40+']]
    
    def dist(r1, r2):
        d = 0
        for i in input_indices:
            if isinstance(r1[i], str):
                d += 0 if r1[i] == r2[i] else 1
            else:
                # Simple Euclidean distance for normalized numeric inputs
                d += (r1[i] - r2[i])**2
        return d**0.5

    # Calculate distances to all rows (excluding the target itself if present)
    distances = []
    for i, row in enumerate(rows):
        if row == target_row:
            continue
        distances.append((dist(row, target_row), i))
    
    distances.sort()
    return [idx for _, idx in distances[:n]]

def remember(header, rows):
    """
    Returns the top 5% of rows based on multi-objective optimization.
    """
    return base_remember(header, rows)

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [val if header[i] == 'criterion' else float(val) 
                             for i, val in enumerate(row)]
            rows.append(processed_row)

    # Assume the "team's current setup" is the last row in the dataset
    current_setup = rows[-1]
    
    # Find 5 most similar setups
    similar_indices = find_similar(header, rows, current_setup, n=5)
    
    # Calculate scores for context (using logic from step01)
    best_indices = base_remember(header, rows)
    
    print("Team's current setup (last row):")
    print(current_setup)
    print("\n5 most similar setups found in history:")
    for idx in similar_indices:
        row = rows[idx]
        is_top = " (Top 5% setup)" if idx in best_indices else ""
        print(f"Index {idx}: {row}{is_top}")
