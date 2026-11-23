import csv
import random

def get_score(header, row):
    """Calculates aggregate score: (1 - MRE) + ACC + PRED40."""
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    return (1.0 - float(row[mre_idx])) + float(row[acc_idx]) + float(row[pred_idx])

def race(header, rows, label):
    """
    Compares three strategies: random, first_n, and last_n.
    Total labels used: 16 (random) + 17 (first_n) + 17 (last_n) = 50.
    """
    budget = 50
    tried = ["random", "first_n", "last_n"]
    results = {}
    
    # Helper to evaluate a row
    def evaluate(idx):
        goals = label(idx)
        row = list(rows[idx])
        row[header.index('MRE-')] = goals[0]
        row[header.index('ACC+')] = goals[1]
        row[header.index('PRED40+')] = goals[2]
        return get_score(header, row), idx

    # 1. Random strategy (16 labels)
    random_indices = random.sample(range(len(rows)), 16)
    best_random = max([evaluate(i) for i in random_indices], key=lambda x: x[0])
    results["random"] = best_random

    # 2. First N strategy (17 labels)
    best_first = max([evaluate(i) for i in range(17)], key=lambda x: x[0])
    results["first_n"] = best_first

    # 3. Last N strategy (17 labels)
    best_last = max([evaluate(i) for i in range(len(rows)-17, len(rows))], key=lambda x: x[0])
    results["last_n"] = best_last

    winner = max(results, key=lambda k: results[k][0])
    return {"winner": winner, "row": results[winner][1], "tried": tried}

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = [float(x) if i not in [4] else x for i, x in enumerate(row)]
            rows.append(processed)

    goal_indices = [header.index('MRE-'), header.index('ACC+'), header.index('PRED40+')]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)

    def label(i):
        return [rows[i][idx] for idx in goal_indices]

    outcome = race(header, masked_rows, label)
    
    print(f"Winning strategy: {outcome['winner']}")
    print(f"Best row found at index: {outcome['row']}")
    print(f"Strategies compared: {', '.join(outcome['tried'])}")
    
    if outcome['winner'] != "random":
        print("Conclusion: The structured search strategies outperformed random sampling.")
    else:
        print("Conclusion: Random sampling remains competitive on this dataset.")
