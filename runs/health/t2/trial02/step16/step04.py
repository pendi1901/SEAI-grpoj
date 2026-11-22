import csv
import step01

def flow(header, row, seen):
    """
    Decides if the current row is 'good enough' to stop searching.
    We define 'good enough' as being in the top 5% of the potential 
    distribution based on the historical data (using the logic from step01).
    """
    # If this is the first row, we can't compare, so keep looking
    if not seen:
        return False

    # Identify goal indices
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    # Combine seen rows with current row to establish the current context
    all_rows = seen + [row]
    
    # Calculate normalization bounds from all rows seen so far
    mres = [r[mre_idx] for r in all_rows]
    accs = [r[acc_idx] for r in all_rows]
    preds = [r[pred_idx] for r in all_rows]

    min_mre, max_mre = min(mres), max(mres)
    min_acc, max_acc = min(accs), max(accs)
    min_pred, max_pred = min(preds), max(preds)

    def get_score(r):
        def norm(val, min_v, max_v):
            return (val - min_v) / (max_v - min_v) if max_v > min_v else 0
        
        s_mre = 1 - norm(r[mre_idx], min_mre, max_mre)
        s_acc = norm(r[acc_idx], min_acc, max_acc)
        s_pred = norm(r[pred_idx], min_pred, max_pred)
        return s_mre + s_acc + s_pred

    # If the current row is in the top 5% of what we've seen, stop
    scores = [get_score(r) for r in all_rows]
    current_score = scores[-1]
    
    # Threshold: is current score better than 95% of the seen distribution?
    threshold = sorted(scores)[int(len(scores) * 0.95)]
    
    return current_score >= threshold

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
    found_idx = -1
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            found_idx = i
            break
        seen.append(row)

    print("Customer Inquiry: 'Tell me the moment I have seen one good enough to ship.'")
    if found_idx != -1:
        print(f"Answer: Found a high-quality setup at row {found_idx + 1}.")
        print(f"MRE={rows[found_idx][0]:.4f}, ACC={rows[found_idx][1]:.4f}, PRED40={rows[found_idx][2]:.4f}")
    else:
        print("Answer: No setup met the quality threshold during the build process.")
