import csv
import random

def get_score(row, header):
    """Calculates a score where higher is better."""
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    # Normalize: (1 - MRE) + ACC + PRED
    return (1.0 - row[mre_idx]) + row[acc_idx] + row[pred_idx]

def race(header, rows, label):
    """
    Compares three strategies:
    1. random: Picks 16 random rows.
    2. greedy: Picks the first 17 rows, then picks the best neighbor of the current best.
    3. explore: Picks 17 rows with high variance in input parameters.
    """
    budget = 50
    labeled = {}

    def get_labeled(i):
        if i not in labeled:
            if len(labeled) >= budget:
                return None
            labeled[i] = label(i)
        return labeled[i]

    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), 16)
        best_idx = -1
        best_score = -float('inf')
        for i in indices:
            goals = get_labeled(i)
            if goals is None: break
            row = rows[i][:]
            row[0], row[1], row[2] = goals
            score = get_score(row, header)
            if score > best_score:
                best_score, best_idx = score, i
        return best_idx, best_score

    # Strategy 2: Greedy (First 17)
    def strategy_greedy():
        best_idx = -1
        best_score = -float('inf')
        for i in range(17):
            goals = get_labeled(i)
            if goals is None: break
            row = rows[i][:]
            row[0], row[1], row[2] = goals
            score = get_score(row, header)
            if score > best_score:
                best_score, best_idx = score, i
        return best_idx, best_score

    # Strategy 3: Explore (Pick rows with high N_estimators)
    def strategy_explore():
        n_est_idx = header.index('N_estimators')
        sorted_indices = sorted(range(len(rows)), key=lambda i: rows[i][n_est_idx], reverse=True)
        best_idx = -1
        best_score = -float('inf')
        for i in sorted_indices[:17]:
            goals = get_labeled(i)
            if goals is None: break
            row = rows[i][:]
            row[0], row[1], row[2] = goals
            score = get_score(row, header)
            if score > best_score:
                best_score, best_idx = score, i
        return best_idx, best_score

    strategies = {
        "random": strategy_random,
        "greedy": strategy_greedy,
        "explore": strategy_explore
    }

    results = {}
    for name, func in strategies.items():
        idx, score = func()
        results[name] = (idx, score)

    winner = max(results, key=lambda n: results[n][1])
    return {"winner": winner, "row": results[winner][0], "tried": list(strategies.keys())}

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = [val if header[i] == 'criterion' else float(val) for i, val in enumerate(row)]
            rows.append(processed)

    true_goals = [[r[0], r[1], r[2]] for r in rows]
    def label(i): return true_goals[i]

    masked_rows = [r[:] for r in rows]
    for r in masked_rows: r[0], r[1], r[2] = "?", "?", "?"

    result = race(header, masked_rows, label)
    print(f"Race complete. Winner: {result['winner']} (found at index {result['row']}).")
    print(f"Strategies compared: {', '.join(result['tried'])}.")
