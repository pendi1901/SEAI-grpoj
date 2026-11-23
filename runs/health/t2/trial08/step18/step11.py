import csv
from step01 import remember as base_remember

def remember(header, rows):
    """
    Returns the top 5% of rows based on the multi-objective optimization logic.
    """
    return base_remember(header, rows)

def find_similar_setups(target_row, all_rows, header, top_n=5):
    """
    Finds the top_n rows most similar to target_row using Euclidean distance
    on input columns.
    """
    input_indices = [i for i, h in enumerate(header) 
                     if not (h.endswith('-') or h.endswith('+'))]
    
    def dist(r1, r2):
        d = 0
        for i in input_indices:
            if isinstance(r1[i], str):
                d += 0 if r1[i] == r2[i] else 1
            else:
                d += (r1[i] - r2[i]) ** 2
        return d**0.5

    # Calculate distances to all rows
    distances = []
    for i, row in enumerate(all_rows):
        distances.append((i, dist(target_row, row)))
    
    # Sort by distance
    distances.sort(key=lambda x: x[1])
    return distances[1:top_n+1] # Skip the first one as it is the target itself

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed = [val if header[i] == 'criterion' else float(val) 
                             for i, val in enumerate(row)]
                rows.append(processed)
        
        # Use the last row as the "team's current setup"
        target_row = rows[-1]
        
        # Find similar setups
        similar = find_similar_setups(target_row, rows, header)
        
        # Calculate scores for context
        best_indices = remember(header, rows)
        
        print("Analysis: Setups most similar to the team's current configuration:")
        for idx, d in similar:
            status = "Top-performing" if idx in best_indices else "Standard"
            print(f"- Row {idx}: Distance {d:.2f}, Status: {status}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
