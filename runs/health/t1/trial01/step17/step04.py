import csv

def flow(header, row, seen):
    """
    Decides whether to stop at the current row based on a threshold strategy.
    We define a 'good' row as one that ranks in the top 5% of the expected 
    distribution of all possible rows.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    # We estimate the global distribution based on the 'seen' data.
    # If we haven't seen enough, we keep looking.
    if len(seen) < 20:
        return False

    def normalize(val, min_v, max_v, reverse=False):
        if max_v == min_v: return 0.5
        norm = (val - min_v) / (max_v - min_v)
        return (1 - norm) if reverse else norm

    # Extract goals from seen data
    mres = [r[mre_idx] for r in seen]
    accs = [r[acc_idx] for r in seen]
    preds = [r[pred_idx] for r in seen]

    # Calculate current row score
    s = (normalize(row[mre_idx], min(mres), max(mres), True) +
         normalize(row[acc_idx], min(accs), max(accs), False) +
         normalize(row[pred_idx], min(preds), max(preds), False)) / 3

    # Calculate scores of seen rows
    seen_scores = []
    for r in seen:
        seen_scores.append((normalize(r[mre_idx], min(mres), max(mres), True) +
                            normalize(r[acc_idx], min(accs), max(accs), False) +
                            normalize(r[pred_idx], min(preds), max(preds), False)) / 3)
    
    # If the current row is better than 95% of what we've seen, we stop.
    threshold = sorted(seen_scores)[int(len(seen_scores) * 0.95)]
    return s >= threshold

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
                    if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 
                                     'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                        processed_row.append(float(val))
                    else:
                        processed_row.append(val)
                rows.append(processed_row)

        seen = []
        found = False
        for i, row in enumerate(rows):
            if flow(header, row, seen):
                print(f"Found a setup good enough to ship at index {i}.")
                print(f"Setup details: {row}")
                found = True
                break
            seen.append(row)
        
        if not found:
            print("No setup met the criteria; processed all available data.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
