import csv

def flow(header, row, seen):
    """
    Decides whether to stop at the current row based on a threshold.
    We define a 'good' row as one that performs better than the 90th percentile
    of the historical data (or the current seen data if small).
    """
    idx_mre = header.index('MRE-')
    idx_acc = header.index('ACC+')
    idx_pred = header.index('PRED40+')

    def get_score(r):
        # Normalize: MRE is minimize (1-val), others maximize (val)
        # Assuming values are in range [0, 1]
        mre = 1.0 - float(r[idx_mre])
        acc = float(r[idx_acc])
        pred = float(r[idx_pred])
        return (mre + acc + pred) / 3.0

    current_score = get_score(row)
    
    # If we have seen enough data, establish a threshold (e.g., top 10%)
    if len(seen) > 20:
        seen_scores = [get_score(r) for r in seen]
        seen_scores.sort(reverse=True)
        threshold = seen_scores[int(len(seen_scores) * 0.10)]
        if current_score >= threshold:
            return True
    
    return False

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed_row = []
                for val in row:
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)

        seen = []
        found = False
        for i, row in enumerate(rows):
            if flow(header, row, seen):
                print(f"Stopped at row {i+1}: Found a setup good enough to ship.")
                found = True
                break
            seen.append(row)
        
        if not found:
            print("Processed all rows; no setup met the shipping criteria.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
