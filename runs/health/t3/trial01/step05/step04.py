import csv

def flow(header, row, seen):
    """
    Decides whether to stop at the current row based on a threshold.
    We define 'good enough' as a row that performs better than 95% of 
    the expected distribution of the data (using the utility function 
    from step01).
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    def get_utility(r):
        # Utility: -MRE + ACC + PRED40
        return -r[mre_idx] + r[acc_idx] + r[pred_idx]

    # If this is the first row, we have no baseline, keep looking
    if not seen:
        return False

    # Calculate utility of current row
    current_utility = get_utility(row)
    
    # Calculate utilities of all seen rows
    seen_utilities = [get_utility(r) for r in seen]
    
    # We define 'good enough' as being in the top 5% of the data.
    # Since we don't know the full distribution, we use the best seen so far
    # as a proxy for the threshold. If the current row is better than 
    # 95% of the previously seen rows, we accept it.
    seen_utilities.sort(reverse=True)
    threshold_idx = max(0, int(len(seen_utilities) * 0.05))
    threshold = seen_utilities[threshold_idx]
    
    return current_utility >= threshold

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
            print(f"Found a good enough setup at index {i}.")
            print(f"Row data: {row}")
            found = True
            break
        seen.append(row)
    
    if not found:
        print("No setup met the criteria before the end of the data.")
