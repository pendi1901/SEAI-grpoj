import csv
from step01 import remember

def flow(header, row, seen):
    """
    Decides whether to stop based on whether the current row is the best 
    seen so far. We define 'best' using the multi-objective scoring 
    logic from step01.
    """
    if not seen:
        return False
    
    # Combine seen rows with the current row to evaluate relative quality
    all_rows = seen + [row]
    
    # Get the indices of the top 5% of the current batch
    best_indices = remember(header, all_rows)
    
    # If the current row (the last one in all_rows) is in the top 5%, 
    # we consider it a significant improvement and stop.
    current_idx = len(all_rows) - 1
    return current_idx in best_indices

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if header[i] not in ['criterion'] else val 
                             for i, val in enumerate(row)]
            rows.append(processed_row)

    seen = []
    found = False
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            print(f"Stopping criteria met at row {i+1}.")
            print("The current setup is among the best observed so far.")
            found = True
            break
        seen.append(row)
    
    if not found:
        print("No setup met the stopping criteria after processing all rows.")
    
    exit(0)
