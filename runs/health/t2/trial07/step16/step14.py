import csv
import step01

def flow(header, row, seen):
    """
    Returns True if the current row is the best seen so far, 
    indicating that the build process has reached a peak and 
    further improvements are unlikely.
    """
    if not seen:
        return True

    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    def get_score(r):
        # Goals: MRE- (min), ACC+ (max), PRED40+ (max)
        # We use a simple linear combination as a proxy for improvement
        # Normalizing is not strictly necessary for identifying the 'best'
        return (-r[mre_idx] + r[acc_idx] + r[pred_idx])

    current_score = get_score(row)
    best_seen_score = max(get_score(r) for r in seen)

    # If the current row is better than anything seen before, 
    # we consider it a new peak.
    return current_score > best_seen_score

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed = [val if header[i] == 'criterion' else float(val) 
                             for i, val in enumerate(row)]
                rows.append(processed)
        
        seen = []
        peaks = 0
        for i, row in enumerate(rows):
            if flow(header, row, seen):
                peaks += 1
                # If we haven't seen a new peak in a long time, we could stop.
                # Here we simply report the discovery of new peaks.
            seen.append(row)
        
        print(f"Analysis complete. Found {peaks} new performance peaks across {len(rows)} runs.")
        print("You can stop paying for runs when the frequency of new peaks drops significantly.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
