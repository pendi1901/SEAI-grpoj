import csv
from step01 import remember

def flow(header, row, seen):
    """
    Decides whether to accept a row based on whether it is 'good'
    relative to the history of rows seen so far.
    """
    # If this is the first row, we have no context, so we wait.
    if not seen:
        return False
    
    # Combine current row with seen rows to evaluate relative performance
    all_rows = seen + [row]
    
    # Use the logic from step01 to identify the best rows
    best_indices = remember(header, all_rows)
    
    # If the current row (the last one in the list) is in the set of best rows,
    # we accept it.
    return (len(all_rows) - 1) in best_indices

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(x) for x in row])
        
        seen = []
        accepted_count = 0
        for row in rows:
            if flow(header, row, seen):
                accepted_count += 1
            seen.append(row)
            
        print(f"Processed {len(rows)} proposals.")
        print(f"Accepted {accepted_count} proposals based on real-time performance analysis.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
