import csv
import step01

def flow(header, row, seen):
    """
    Returns True if the current row is the best seen so far, 
    or if we have seen enough rows that the best score hasn't 
    improved in a significant window (e.g., 10% of the data).
    """
    if not seen:
        return True

    # Use step01 logic to score the current row and all seen rows
    all_rows = seen + [row]
    
    # Calculate scores for all seen rows + current
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    def get_scores(data):
        mres = [r[mre_idx] for r in data]
        accs = [r[acc_idx] for r in data]
        preds = [r[pred_idx] for r in data]
        min_mre, max_mre = min(mres), max(mres)
        min_acc, max_acc = min(accs), max(accs)
        min_pred, max_pred = min(preds), max(preds)
        
        def normalize(val, min_v, max_v, reverse=False):
            if max_v == min_v: return 0.0
            norm = (val - min_v) / (max_v - min_v)
            return (1.0 - norm) if reverse else norm
            
        scores = []
        for r in data:
            s = (normalize(r[mre_idx], min_mre, max_mre, True) +
                 normalize(r[acc_idx], min_acc, max_acc, False) +
                 normalize(r[pred_idx], min_pred, max_pred, False)) / 3.0
            scores.append(s)
        return scores

    scores = get_scores(all_rows)
    current_score = scores[-1]
    best_so_far = max(scores[:-1])
    
    # If current is better than anything seen, keep it
    if current_score > best_so_far:
        return True
        
    # If we have seen a significant number of rows (e.g., 100) 
    # and the best score hasn't improved, stop.
    if len(seen) > 100:
        # Check if the best score has improved in the last 50 rows
        recent_best = max(scores[-50:-1])
        if best_so_far >= recent_best:
            return True
            
    return False

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed = []
                for i, val in enumerate(row):
                    if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 
                                     'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                        processed.append(float(val))
                    else:
                        processed.append(val)
                rows.append(processed)
        
        seen = []
        for i, row in enumerate(rows):
            if flow(header, row, seen):
                # If flow returns True, we consider this a milestone
                # For the customer, we print the index where we stop/update
                if i > 100: # Only report after initial burn-in
                    print(f"Improvement plateaued or new best found at index {i}. Stopping run.")
                    break
            seen.append(row)
        else:
            print("Run completed without finding significant improvements.")
            
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
