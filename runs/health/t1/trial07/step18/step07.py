import csv
import random

def choose(header, rows, label):
    """
    Finds the best setup by sampling 50 rows, labeling them, 
    and returning the index of the best performing one.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    # We have 800 rows, we can label 50.
    # Strategy: Randomly sample 50 rows to get a representative view of the space.
    indices = list(range(len(rows)))
    sample_indices = random.sample(indices, 50)
    
    best_idx = -1
    best_score = -float('inf')
    
    # Normalize goals for scoring
    # Since we only have 50 samples, we use them to estimate global min/max
    labeled_data = []
    for i in sample_indices:
        goals = label(i)
        labeled_data.append((goals, i))
    
    mres = [d[0][0] for d in labeled_data]
    accs = [d[0][1] for d in labeled_data]
    preds = [d[0][2] for d in labeled_data]
    
    min_mre, max_mre = min(mres), max(mres)
    min_acc, max_acc = min(accs), max(accs)
    min_pred, max_pred = min(preds), max(preds)
    
    def normalize(val, min_v, max_v, reverse=False):
        if max_v == min_v: return 0.5
        norm = (val - min_v) / (max_v - min_v)
        return (1 - norm) if reverse else norm

    for goals, i in labeled_data:
        # Score = average of normalized goals
        s = (normalize(goals[0], min_mre, max_mre, True) +
             normalize(goals[1], min_acc, max_acc) +
             normalize(goals[2], min_pred, max_pred)) / 3
        
        if s > best_score:
            best_score = s
            best_idx = i
            
    return best_idx

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    rows = []
    full_data = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = []
            for i, val in enumerate(row):
                if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 
                                 'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                    processed.append(float(val))
                else:
                    processed.append(val)
            full_data.append(processed)
            
            # Create masked row for the function
            masked = list(processed)
            masked[0] = "?"
            masked[1] = "?"
            masked[2] = "?"
            rows.append(masked)

    def label(i):
        return [full_data[i][0], full_data[i][1], full_data[i][2]]

    best_idx = choose(header, rows, label)
    
    print(f"Analysis complete. Best setup found at index {best_idx}.")
    print(f"MRE: {full_data[best_idx][0]:.4f}, ACC: {full_data[best_idx][1]:.4f}, PRED40: {full_data[best_idx][2]:.4f}")
