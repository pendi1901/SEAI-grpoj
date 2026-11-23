import csv
import step01
import step02
import step06

def choose(header, rows, label):
    """
    Finds the best setup by sampling 50 rows, labeling them, 
    and picking the one with the highest multi-objective score.
    """
    # We have 800 rows, we can label 50.
    # We pick 50 indices spread across the dataset to get a good representation.
    n = len(rows)
    indices_to_label = [int(i * (n / 50)) for i in range(50)]
    
    best_idx = -1
    best_score = -float('inf')
    
    # Pre-calculate min/max for normalization based on the 50 samples
    # Since we don't know the full range, we use the samples as a proxy
    labeled_data = []
    for i in indices_to_label:
        goals = label(i)
        # Create a full row with goals filled in
        full_row = goals + rows[i][len(goals):]
        labeled_data.append(full_row)
        
    # Use step01 logic to score the labeled rows
    # We need to adapt step01's logic to work on our labeled subset
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    mres = [r[mre_idx] for r in labeled_data]
    accs = [r[acc_idx] for r in labeled_data]
    preds = [r[pred_idx] for r in labeled_data]
    
    min_mre, max_mre = min(mres), max(mres)
    min_acc, max_acc = min(accs), max(accs)
    min_pred, max_pred = min(preds), max(preds)
    
    def normalize(val, min_v, max_v, reverse=False):
        if max_v == min_v: return 0.0
        norm = (val - min_v) / (max_v - min_v)
        return 1.0 - norm if reverse else norm

    for i, row in enumerate(labeled_data):
        s = (normalize(row[mre_idx], min_mre, max_mre, True) +
             normalize(row[acc_idx], min_acc, max_acc) +
             normalize(row[pred_idx], min_pred, max_pred))
        
        if s > best_score:
            best_score = s
            best_idx = indices_to_label[i]
            
    return best_idx

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed_row = [val if header[i] == 'criterion' else float(val) 
                                 for i, val in enumerate(row)]
                rows.append(processed_row)
        
        # Create a hidden version for the harness
        hidden_rows = [["?"] * 3 + r[3:] for r in rows]
        
        def label(i):
            return rows[i][:3]
            
        best_idx = choose(header, hidden_rows, label)
        print(f"The best setup found is at index {best_idx}.")
        print(f"MRE={rows[best_idx][0]:.4f}, ACC={rows[best_idx][1]:.4f}, PRED40={rows[best_idx][2]:.4f}")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
