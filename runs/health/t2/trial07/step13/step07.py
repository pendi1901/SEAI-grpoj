import csv
import step01
import step02

def choose(header, rows, label):
    """
    Finds the best setup by sampling 50 rows, labeling them, 
    and picking the one with the highest multi-objective score.
    """
    # We have 800 rows. We can label 50.
    # We'll pick 50 indices spread across the dataset.
    indices = [int(i * (len(rows) - 1) / 49) for i in range(50)]
    
    labeled_data = []
    for i in indices:
        # Get true goals
        goals = label(i)
        # Reconstruct row with true goals
        row = list(rows[i])
        goal_indices = [j for j, h in enumerate(header) if h.endswith(('-', '+'))]
        for idx, g_val in zip(goal_indices, goals):
            row[idx] = g_val
        labeled_data.append((row, i))
    
    # Use step01 logic to score these 50 rows
    # We need to pass a list of rows to step01.remember, but it expects 
    # the full dataset. We adapt by creating a mini-dataset of our 50.
    
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    mres = [r[0][mre_idx] for r in labeled_data]
    accs = [r[0][acc_idx] for r in labeled_data]
    preds = [r[0][pred_idx] for r in labeled_data]
    
    min_mre, max_mre = min(mres), max(mres)
    min_acc, max_acc = min(accs), max(accs)
    min_pred, max_pred = min(preds), max(preds)
    
    def normalize(val, min_v, max_v, reverse=False):
        if max_v == min_v: return 0.5
        norm = (val - min_v) / (max_v - min_v)
        return (1 - norm) if reverse else norm
    
    best_score = -1
    best_idx = -1
    
    for row, original_idx in labeled_data:
        s = (normalize(row[mre_idx], min_mre, max_mre, True) +
             normalize(row[acc_idx], min_acc, max_acc, False) +
             normalize(row[pred_idx], min_pred, max_pred, False)) / 3
        if s > best_score:
            best_score = s
            best_idx = original_idx
            
    return best_idx

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = [val if header[i] == 'criterion' else float(val) for i, val in enumerate(row)]
            rows.append(processed)
            
    # Mock label function for the standalone execution
    def label(i):
        # Return the goal values from the original row
        return [rows[i][0], rows[i][1], rows[i][2]]
    
    # Hide goals for the choose function
    hidden_rows = [[val if i > 2 else "?" for i, val in enumerate(r)] for r in rows]
    
    best_idx = choose(header, hidden_rows, label)
    print(f"The best setup found is at index {best_idx}.")
