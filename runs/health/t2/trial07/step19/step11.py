import csv
import step01
import step02

def remember(header, rows):
    """
    Finds the setups most similar to the current setup (the last row in the dataset)
    and returns their indices, ranked by their multi-objective score.
    """
    # Identify the current setup (last row)
    current_setup = rows[-1]
    
    # Identify goal and input indices
    goal_indices = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
    input_indices = [i for i in range(len(header)) if i not in goal_indices]

    # Calculate distance to current setup for all rows
    def dist(row1, row2):
        d = 0
        for i in input_indices:
            v1, v2 = row1[i], row2[i]
            if isinstance(v1, str):
                d += 0 if v1 == v2 else 1
            else:
                # Normalize numeric distance
                d += (v1 - v2)**2
        return d**0.5

    # Calculate scores for all rows using step01 logic
    best_indices = step01.remember(header, rows)
    
    # Find rows most similar to the current setup (excluding the current setup itself)
    distances = []
    for i in range(len(rows) - 1):
        d = dist(current_setup, rows[i])
        distances.append((d, i))
    
    # Sort by distance ascending (most similar first)
    distances.sort(key=lambda x: x[0])
    
    # Return the top 5% of rows that are most similar
    limit = max(1, int(len(rows) * 0.05))
    return [item[1] for item in distances[:limit]]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed = [val if header[i] == 'criterion' else float(val) 
                             for i, val in enumerate(row)]
                rows.append(processed)
        
        indices = remember(header, rows)
        
        print("The setups most similar to your current configuration are:")
        for idx in indices:
            # Calculate a simple score for display
            mre = rows[idx][header.index('MRE-')]
            acc = rows[idx][header.index('ACC+')]
            print(f"Row {idx}: MRE={mre:.4f}, ACC={acc:.4f}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
