import csv
import step01
import step02

def choose(header, rows, label):
    """
    Finds the best setup by sampling 50 rows. 
    We use a simple strategy: evaluate the first 50 rows, 
    then pick the one with the highest multi-objective score.
    """
    # We can label at most 50 rows.
    n_to_sample = min(50, len(rows))
    
    # Label the first n_to_sample rows
    for i in range(n_to_sample):
        goals = label(i)
        rows[i][0] = goals[0] # MRE-
        rows[i][1] = goals[1] # ACC+
        rows[i][2] = goals[2] # PRED40+
        
    # Use step01 logic to score the labeled rows
    # We only consider the rows we have labeled
    labeled_rows = rows[:n_to_sample]
    
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    mres = [r[mre_idx] for r in labeled_rows]
    accs = [r[acc_idx] for r in labeled_rows]
    preds = [r[pred_idx] for r in labeled_rows]
    
    min_mre, max_mre = min(mres), max(mres)
    min_acc, max_acc = min(accs), max(accs)
    min_pred, max_pred = min(preds), max(preds)
    
    def normalize(val, min_v, max_v, reverse=False):
        if max_v == min_v: return 0.5
        norm = (val - min_v) / (max_v - min_v)
        return 1.0 - norm if reverse else norm
    
    best_idx = -1
    best_score = -1.0
    
    for i in range(n_to_sample):
        s1 = normalize(rows[i][mre_idx], min_mre, max_mre, reverse=True)
        s2 = normalize(rows[i][acc_idx], min_acc, max_acc)
        s3 = normalize(rows[i][pred_idx], min_pred, max_pred)
        score = (s1 + s2 + s3) / 3.0
        
        if score > best_score:
            best_score = score
            best_idx = i
            
    return best_idx

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [val if header[i] == 'criterion' else float(val) for i, val in enumerate(row)]
            rows.append(processed_row)
            
    # Keep a copy of true goals to simulate the label function
    true_goals = [[r[0], r[1], r[2]] for r in rows]
    
    def label(i):
        return true_goals[i]
    
    # Mask goals
    for r in rows:
        r[0] = r[1] = r[2] = "?"
        
    best_idx = choose(header, rows, label)
    print(f"The best setup found within 50 trials is at index {best_idx}.")
    print(f"Performance: MRE={true_goals[best_idx][0]:.4f}, ACC={true_goals[best_idx][1]:.4f}, PRED40={true_goals[best_idx][2]:.4f}")
