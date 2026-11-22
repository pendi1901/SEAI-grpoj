import csv
import step01

def flow(header, row, seen):
    """
    Decides whether to stop based on whether the current row is the best 
    seen so far. We use the multi-objective scoring logic from step01.
    If the current row's score is higher than any previous row, we stop.
    """
    if not seen:
        return True

    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    # Combine all seen rows to establish the current normalization context
    all_rows = seen + [row]
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

    # Calculate scores for all seen rows
    scores = [get_score(r) for r in all_rows]
    
    # If the current row (the last one) has the highest score, we stop
    return scores[-1] >= max(scores[:-1])

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
    stop_idx = -1
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            # If the logic says stop, we record the index and break
            stop_idx = i
            break
        seen.append(row)

    print("Customer Inquiry: 'Tell me when the best so far has stopped improving, so I can stop paying for runs.'")
    if stop_idx != -1:
        print(f"Answer: The best setup was found at run {stop_idx + 1}. You can stop paying for further runs.")
    else:
        print("Answer: No improvement detected.")
