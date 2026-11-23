import csv
import random

def choose(header, rows, label):
    """
    Finds the best setup by sampling 50 rows, labeling them,
    and returning the index of the one with the highest multi-objective score.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    # We have 800 rows, we can label 50.
    # We pick 50 random indices to sample the space.
    indices = random.sample(range(len(rows)), 50)
    
    best_idx = -1
    best_score = -1.0
    
    # Track values to normalize scores
    labeled_data = []
    for i in indices:
        goals = label(i)
        labeled_data.append((goals[0], goals[1], goals[2]))
        
    mres = [d[0] for d in labeled_data]
    accs = [d[1] for d in labeled_data]
    preds = [d[2] for d in labeled_data]
    
    min_mre, max_mre = min(mres), max(mres)
    min_acc, max_acc = min(accs), max(accs)
    min_pred, max_pred = min(preds), max(preds)
    
    def norm(val, min_v, max_v, reverse=False):
        if max_v == min_v: return 0.0
        n = (val - min_v) / (max_v - min_v)
        return 1.0 - n if reverse else n

    for i, (mre, acc, pred) in enumerate(labeled_data):
        s1 = norm(mre, min_mre, max_mre, reverse=True)
        s2 = norm(acc, min_acc, max_acc)
        s3 = norm(pred, min_pred, max_pred)
        score = (s1 + s2 + s3) / 3.0
        
        if score > best_score:
            best_score = score
            best_idx = indices[i]
            
    return best_idx

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            true_goals = []
            for row in reader:
                # Store true goals separately and mask them in rows
                true_goals.append([float(row[0]), float(row[1]), float(row[2])])
                processed = [val if header[i] == 'criterion' else float(val) 
                             for i, val in enumerate(row)]
                # Mask goals
                for idx in [0, 1, 2]:
                    processed[idx] = "?"
                rows.append(processed)

        def label(i):
            return true_goals[i]

        best_row_idx = choose(header, rows, label)
        print(f"The best configuration found is at row index {best_row_idx}.")
        print(f"True goals for this setup: MRE={true_goals[best_row_idx][0]:.4f}, "
              f"ACC={true_goals[best_row_idx][1]:.4f}, PRED={true_goals[best_row_idx][2]:.4f}")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
