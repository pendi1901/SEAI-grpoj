import csv

def flow(header, row, seen):
    """
    Decides whether to accept the current row based on whether it is 
    better than all previously seen rows across all goals.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    # If this is the first row, we have no baseline, so keep looking
    if not seen:
        return False

    # A row is "good enough" if it dominates or is better than the best 
    # seen so far. We define "better" as having a better composite score 
    # than any previous row.
    def get_score(r):
        # We don't have global min/max here, so we compare relative to 
        # the current row's performance against the seen set.
        # Simple heuristic: is this row better than the best seen?
        return (-r[mre_idx], r[acc_idx], r[pred_idx])

    current_score = get_score(row)
    best_seen_score = max([get_score(r) for r in seen])

    # If current row is better than the best seen, we stop.
    return current_score > best_seen_score

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed = [float(val) if header[i] not in ['criterion'] else val 
                             for i, val in enumerate(row)]
                rows.append(processed)

        seen = []
        found = False
        for i, row in enumerate(rows):
            if flow(header, row, seen):
                print(f"Found a good setup at row {i+1}.")
                print(f"Values: MRE-={row[0]:.4f}, ACC+={row[1]:.4f}, PRED40+={row[2]:.4f}")
                found = True
                break
            seen.append(row)
        
        if not found:
            print("No setup met the criteria.")
            
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
