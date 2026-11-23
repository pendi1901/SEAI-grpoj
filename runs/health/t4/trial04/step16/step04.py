import csv
from step01 import remember

def flow(header, row, seen):
    """
    Decides whether to accept the current row based on whether it is 
    better than all previously seen rows.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    def get_score(r):
        # Higher score is better: minimize MRE, maximize ACC, maximize PRED40
        return (1.0 - float(r[mre_idx])) + float(r[acc_idx]) + float(r[pred_idx])

    current_score = get_score(row)
    
    # If this is the first row, we don't have a baseline, so we keep looking
    if not seen:
        return False
    
    # Compare against the best seen so far
    best_seen_score = max(get_score(r) for r in seen)
    
    # If current row is better than the best seen, we stop and ship it
    return current_score > best_seen_score

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
            print(f"Found a setup good enough to ship at index {i}!")
            print(f"Row details: {row}")
            found = True
            break
        seen.append(row)
    
    if not found:
        print("No setup found that outperformed all previous ones.")
