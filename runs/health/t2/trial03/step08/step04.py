import csv
from step01 import remember

def flow(header, row, seen):
    """
    Decides if the current row is 'good enough' to ship.
    We define 'good enough' as being in the top 5% of the expected 
    distribution of all rows, based on the logic from step01.
    """
    # If this is the first row, we cannot compare yet
    if not seen:
        return False
    
    # Combine seen rows with current row to establish context
    all_rows = seen + [row]
    
    # Use the remember logic to identify the top 5% indices
    # We need to handle the fact that 'remember' expects a full list
    best_indices = remember(header, all_rows)
    
    # If the current row (the last one in all_rows) is in the top 5%, ship it
    current_idx = len(all_rows) - 1
    return current_idx in best_indices

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

    seen = []
    shipped = False
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            print(f"Shipped setup at index {i} (row {i+1}).")
            shipped = True
            break
        seen.append(row)
    
    if not shipped:
        print("No setup met the criteria for shipping.")
