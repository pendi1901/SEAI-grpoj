import csv
import random

def race(header, rows, label):
    """
    Compares three strategies:
    1. random: Picks 16 random rows.
    2. greedy: Picks 17 rows by exploring neighbors of the best found so far.
    3. explore: Picks 17 rows by sampling the edges of the input space.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    budget = 50
    labeled = {}

    def get_score(goals):
        # Normalize goals: MRE (min), ACC (max), PRED40 (max)
        # Since we don't have global bounds, we use a simple heuristic
        return (-goals[0] + goals[1] + goals[2])

    def get_label(i):
        if i not in labeled:
            if len(labeled) >= budget:
                raise Exception("Budget exceeded")
            labeled[i] = label(i)
        return labeled[i]

    # 1. Random Strategy
    def strategy_random():
        indices = random.sample(range(len(rows)), 16)
        best_idx = -1
        best_score = -float('inf')
        for i in indices:
            s = get_score(get_label(i))
            if s > best_score:
                best_score, best_idx = s, i
        return best_idx

    # 2. Greedy Strategy
    def strategy_greedy():
        curr = random.randint(0, len(rows) - 1)
        for _ in range(16):
            neighbors = random.sample(range(len(rows)), 5)
            best_n = -1
            best_s = -float('inf')
            for n in neighbors:
                s = get_score(get_label(n))
                if s > best_s:
                    best_s, best_n = s, n
            if best_s > get_score(get_label(curr)):
                curr = best_n
        return curr

    # 3. Explore Strategy (Focus on extreme values)
    def strategy_explore():
        # Pick rows with extreme values in N_estimators
        n_idx = header.index('N_estimators')
        vals = [(rows[i][n_idx], i) for i in range(len(rows))]
        vals.sort()
        indices = [v[1] for v in vals[:8]] + [v[1] for v in vals[-9:]]
        best_idx = -1
        best_score = -float('inf')
        for i in indices:
            s = get_score(get_label(i))
            if s > best_score:
                best_score, best_idx = s, i
        return best_idx

    results = {
        "random": strategy_random(),
        "greedy": strategy_greedy(),
        "explore": strategy_explore()
    }

    best_overall = -float('inf')
    winner = ""
    best_row_idx = -1

    for name, idx in results.items():
        score = get_score(get_label(idx))
        if score > best_overall:
            best_overall = score
            winner = name
            best_row_idx = idx

    return {"winner": winner, "row": best_row_idx, "tried": ["random", "greedy", "explore"]}

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    full_data = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = [float(val) if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth'] else val for i, val in enumerate(row)]
            full_data.append(processed)

    def label(i):
        return [full_data[i][0], full_data[i][1], full_data[i][2]]

    rows = []
    for r in full_data:
        masked = list(r)
        masked[0] = masked[1] = masked[2] = "?"
        rows.append(masked)

    result = race(header, rows, label)
    print(f"Race Results: The winner is '{result['winner']}' strategy.")
    print(f"Best row found at index {result['row']} with goals: {full_data[result['row']][:3]}")
    print(f"Strategies compared: {', '.join(result['tried'])}")
