import csv
from step01 import remember

def flow(header, row, seen):
    """
    Returns True if the current row is the best seen so far, 
    signaling that we have reached a peak in performance.
    """
    if not seen:
        return True
    
    # Combine all rows to evaluate the current row's relative rank
    all_rows = seen + [row]
    best_indices = remember(header, all_rows)
    
    # If the current row (the last one) is in the top 5% of all seen so far,
    # we consider it a 'best' and stop.
    return (len(all_rows) - 1) in best_indices

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
    stopped = False
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            # If we stop, we report the index
            print(f"The best setup stopped improving at run {i + 1} (index {i}).")
            print(f"Setup details: {row}")
            stopped = True
            break
        seen.append(row)
    
    if not stopped:
        print("The runs continued without finding a significant improvement peak.")
