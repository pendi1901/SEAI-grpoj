import csv
import random
from step01 import remember

def get_score(header, row):
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    return (1.0 - float(row[mre_idx])) + float(row[acc_idx]) + float(row[pred_idx])

def race(header, rows, label):
    """
    Compares three strategies: random, greedy (first 17), and top-k (last 16).
    Total budget: 50 labels.
    """
    strategies = ["random", "greedy", "top-k"]
    results = {}
    
    # Strategy 1: Random
    indices_random = random.sample(range(len(rows)), 17)
    best_r = -1
    best_s_r = -float('inf')
    for i in indices_random:
        goals = label(i)
        row = [goals[0], goals[1], goals[2]] + rows[i][3:]
        score = get_score(header, row)
        if score > best_s_r:
            best_s_r = score
            best_r = i
    results["random"] = (best_s_r, best_r)

    # Strategy 2: Greedy (first 17)
    indices_greedy = list(range(17))
    best_g = -1
    best_s_g = -float('inf')
    for i in indices_greedy:
        goals = label(i)
        row = [goals[0], goals[1], goals[2]] + rows[i][3:]
        score = get_score(header, row)
        if score > best_s_g:
            best_s_g = score
            best_g = i
    results["greedy"] = (best_s_g, best_g)

    # Strategy 3: Top-k (last 16)
    indices_top = list(range(len(rows)-16, len(rows)))
    best_t = -1
    best_s_t = -float('inf')
    for i in indices_top:
        goals = label(i)
        row = [goals[0], goals[1], goals[2]] + rows[i][3:]
        score = get_score(header, row)
        if score > best_s_t:
            best_s_t = score
            best_t = i
    results["top-k"] = (best_s_t, best_t)

    winner = max(results, key=lambda k: results[k][0])
    return {"winner": winner, "row": results[winner][1], "tried": strategies}

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i] == 'criterion':
                    processed_row.append(val)
                else:
                    processed_row.append(float(val))
            rows.append(processed_row)

    full_data = [r[:] for r in rows]
    masked_rows = []
    for r in rows:
        m = r[:]
        m[0] = m[1] = m[2] = "?"
        masked_rows.append(m)

    def label(i):
        return [full_data[i][0], full_data[i][1], full_data[i][2]]

    outcome = race(header, masked_rows, label)
    print(f"Race complete. Winner: {outcome['winner']} (found at row {outcome['row']}).")
    print(f"Strategies compared: {', '.join(outcome['tried'])}.")
