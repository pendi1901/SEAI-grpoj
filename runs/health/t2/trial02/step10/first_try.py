import csv
import random
import step01

def race(header, rows, label):
    """
    Compares three strategies for finding the best setup with a 50-label budget.
    Budget is split: 16 labels for each of the 3 strategies.
    """
    budget = 50
    per_strategy = budget // 3
    
    # Helper to evaluate a row
    def get_score(row):
        mre_idx = header.index('MRE-')
        acc_idx = header.index('ACC+')
        pred_idx = header.index('PRED40+')
        
        # Normalize logic from step01
        mres = [r[mre_idx] for r in rows if r[mre_idx] != '?']
        accs = [r[acc_idx] for r in rows if r[acc_idx] != '?']
        preds = [r[pred_idx] for r in rows if r[pred_idx] != '?']
        
        def norm(val, min_v, max_v):
            return (val - min_v) / (max_v - min_v) if max_v > min_v else 0
        
        s_mre = 1 - norm(row[mre_idx], min(mres), max(mres))
        s_acc = norm(row[acc_idx], min(accs), max(accs))
        s_pred = norm(row[pred_idx], min(pred_idx), max(pred_idx))
        return s_mre + s_acc + s_pred

    results = {}
    
    # 1. Random Strategy
    random_indices = random.sample(range(len(rows)), per_strategy)
    best_r = -1
    best_s_r = -float('inf')
    for i in random_indices:
        goals = label(i)
        rows[i][0], rows[i][1], rows[i][2] = goals
        score = get_score(rows[i])
        if score > best_s_r:
            best_s_r, best_r = score, i
    results["random"] = (best_s_r, best_r)

    # 2. First-N Strategy
    first_indices = list(range(per_strategy))
    best_f = -1
    best_s_f = -float('inf')
    for i in first_indices:
        goals = label(i)
        rows[i][0], rows[i][1], rows[i][2] = goals
        score = get_score(rows[i])
        if score > best_s_f:
            best_s_f, best_f = score, i
    results["first_n"] = (best_s_f, best_f)

    # 3. Last-N Strategy
    last_indices = list(range(len(rows) - per_strategy, len(rows)))
    best_l = -1
    best_s_l = -float('inf')
    for i in last_indices:
        goals = label(i)
        rows[i][0], rows[i][1], rows[i][2] = goals
        score = get_score(rows[i])
        if score > best_s_l:
            best_s_l, best_l = score, i
    results["last_n"] = (best_s_l, best_l)

    winner = max(results, key=lambda k: results[k][0])
    return {"winner": winner, "row": results[winner][1], "tried": ["random", "first_n", "last_n"]}

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rows.append([val if header[i] == 'criterion' else float(val) for i, val in enumerate(row)])

    true_data = [r[:] for r in rows]
    for r in rows:
        r[0], r[1], r[2] = "?", "?", "?"

    def label(i):
        return [true_data[i][0], true_data[i][1], true_data[i][2]]

    outcome = race(header, rows, label)
    print(f"Race complete. Winner: {outcome['winner']} at row {outcome['row']}.")
