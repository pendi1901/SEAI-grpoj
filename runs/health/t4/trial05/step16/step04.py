import csv
from step01 import remember

def flow(header, row, seen):
    """
    Decides if the current row is 'good enough' to stop.
    We define 'good enough' as being in the top 5% of the entire dataset,
    as determined by the remember() function in step01.
    """
    # Combine seen rows with the current row to evaluate relative quality
    all_rows = seen + [row]
    
    # Get the indices of the top 5% of the current batch
    best_indices = remember(header, all_rows)
    
    # If the current row (the last one in all_rows) is in the top 5%, stop.
    current_idx = len(all_rows) - 1
    return current_idx in best_indices

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i] == 'criterion':
                    processed_row.append(val)
                else:
                    processed_row.append(float(val))
            rows.append(processed_row)

    seen = []
    found = False
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            print(f"Found a good setup at row {i+1}. Stopping.")
            found = True
            break
        seen.append(row)
    
    if not found:
        print("No setup met the criteria.")
    
    exit(0)
