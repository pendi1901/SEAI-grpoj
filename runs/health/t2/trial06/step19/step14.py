import csv

def flow(header, row, seen):
    """
    Returns True if the current row is the best seen so far, 
    signaling that we have reached a local optimum and can stop.
    """
    if not seen:
        return False

    # Identify goal indices
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    def get_score(r):
        # Goals: MRE- (min), ACC+ (max), PRED40+ (max)
        # We use raw values here as we are comparing relative to history
        return -r[mre_idx] + r[acc_idx] + r[pred_idx]

    current_score = get_score(row)
    best_seen_score = max(get_score(r) for r in seen)

    # If the current row is better than anything seen before, 
    # we consider it an improvement. If it's not, we might be at a plateau.
    # To answer "when it stopped improving", we return True if it's the new best.
    return current_score > best_seen_score

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
        if i > 0 and flow(header, row, seen):
            # This row is a new best, so we haven't stopped improving yet.
            pass
        elif i > 100: 
            # Simple heuristic: if we haven't seen a new best in a while, stop.
            # For the purpose of this script, we report the last time we saw an improvement.
            print(f"Improvement trend analysis: The last significant improvement was at row {i}.")
            stopped = True
            break
        seen.append(row)

    if not stopped:
        print("The system is still finding improvements.")
