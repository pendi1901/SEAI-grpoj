import csv
import random

def race(header, rows, label):
    """
    Compares three strategies:
    1. random: Samples 16 random rows.
    2. greedy: Starts at a random row, samples 16 neighbors, moves to better ones.
    3. extreme: Samples 18 rows with extreme values in N_estimators.
    Total budget: 50 labels.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    n_est_idx = header.index('N_estimators')
    
    budget = 50
    labeled = {}

    def get_score(goals):
        # Normalize goals: MRE (min), ACC (max), PRED40 (max)
        # Score = -MRE + ACC + PRED40
        return (-goals[0] + goals[1] + goals[2])

    def get_label(i):
        if i not in labeled:
            if len(labeled) >= budget:
                return None
            labeled[i] = label(i)
        return labeled[i]

    # 1. Random Strategy
    def strategy_random():
        indices = random.sample(range(len(rows)), 16)
        best_idx, best_score = -1, -float('inf')
        for i in indices:
            goals = get_label(i)
            if goals is not None:
                s = get_score(goals)
                if s > best_score:
                    best_score, best_idx = s, i
        return best_idx

    # 2. Greedy Strategy
    def strategy_greedy():
        curr = random.randint(0, len(rows) - 1)
        best_idx, best_score = curr, -float('inf')
        
        for _ in range(16):
            goals_curr = get_label(curr)
            if goals_curr is None: break
            
            s_curr = get_score(goals_curr)
            if s_curr > best_score:
                best_score, best_idx = s_curr, curr
                
            neighbors = random.sample(range(len(rows)), 3)
            for n in neighbors:
                goals_n = get_label(n)
                if goals_n is not None:
                    s_n = get_score(goals_n)
                    if s_n > s_curr:
                        curr = n
                        break
        return best_idx

    # 3. Extreme Strategy
    def strategy_extreme():
        vals = sorted([(rows[i][n_est_idx], i) for i in range(len(rows))])
        indices = [v[1] for v in vals[:9]] + [v[1] for v in vals[-9:]]
        best_idx, best_score = -1, -float('inf')
        for i in indices:
            goals = get_label(i)
            if goals is not None:
                s = get_score(goals)
                if s > best_score:
                    best_score, best_idx = s, i
        return best_idx

    results = {
        "random": strategy_random(),
        "greedy": strategy_greedy(),
        "extreme": strategy_extreme()
    }

    best_overall = -float('inf')
    winner = "random"
    best_row_idx = results["random"]

    for name, idx in results.items():
        if idx != -1:
            goals = get_label(idx)
            if goals is not None:
                score = get_score(goals)
                if score > best_overall:
                    best_overall = score
                    winner = name
                    best_row_idx = idx

    return {"winner": winner, "row": best_row_idx, "tried": ["random", "greedy", "extreme"]}

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
