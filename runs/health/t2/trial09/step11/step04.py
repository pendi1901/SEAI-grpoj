import csv
from step01 import remember

def flow(header, row, seen):
    """
    Decides if the current row is 'good enough' to stop searching.
    We define 'good enough' as being in the top 5% of the distribution
    of all rows seen so far, including the current one.
    """
    # Combine previous rows with the current one
    all_rows = seen + [row]
    
    # Use the logic from step01 to identify the top 5%
    # We only care if the current row is in the top 5% of the current set
    top_indices = remember(header, all_rows)
    
    # If the current row (index len(all_rows)-1) is in the top set, stop
    return (len(all_rows) - 1) in top_indices

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
    found_index = -1
    
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            found_index = i
            break
        seen.append(row)
    
    if found_index != -1:
        print(f"Stopped at row {found_index + 1} (1-indexed).")
        print(f"Row data: {rows[found_index]}")
        print("This setup meets the criteria for immediate deployment.")
    else:
        print("No setup met the criteria before the end of the data.")
