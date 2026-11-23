import csv
from step01 import remember

def flow(header, row, seen):
    """
    Decides whether to accept the current row based on whether it is 
    statistically 'good enough' compared to the history of seen rows.
    We define 'good enough' as being in the top 5% of the combined 
    set of seen rows and the current row.
    """
    if not seen:
        return False
    
    # Combine seen rows with the current row
    all_rows = seen + [row]
    
    # Use the logic from step01 to identify the top 5%
    best_indices = remember(header, all_rows)
    
    # If the current row (the last index) is in the top 5%, we accept it
    return (len(all_rows) - 1) in best_indices

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
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
                print(f"Found a setup good enough to ship at index {i}.")
                found = True
                break
            seen.append(row)
            
        if not found:
            print("No setup met the criteria for shipping.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
