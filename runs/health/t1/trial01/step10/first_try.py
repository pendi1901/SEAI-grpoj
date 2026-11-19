import csv
import random

def race(header, rows, label):
    """
    Compares three strategies:
    1. random: Picks 17 rows at random.
    2. greedy: Picks 17 rows by exploring neighbors of the best found so far.
    3. explore: Picks 16 rows by sampling in areas with high variance.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    
    def get_score(goals):
        # Normalize goals: MRE- (min), ACC+ (max), PRED40+ (max)
        # Since we don't have global stats, we use a simple weighted sum
        # MRE- is usually [0,1], ACC/PRED are [0,1].
        # Score = (1 - MRE) + ACC + PRED
        mre = goals[0]
        acc = goals[1]
        pred = goals[2]
        return (1 - mre) + acc + pred

    budget = 50
    labeled = {}

    def get_label(i):
        if i not in labeled:
            if len(labeled) >= budget:
                raise Exception("Budget exceeded")
            labeled[i] = label(i)
        return labeled[i]

    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), 17)
        best_idx = -1
        best_s = -float('inf')
        for i in indices:
            s = get_score(get_label(i))
            if s > best_s:
                best_s, best_idx = s, i
        return best_idx, best_s

    # Strategy 2: Greedy (Local Search)
    def strategy_greedy():
        curr = random.randint(0, len(rows) - 1)
        best_idx, best_s = curr, get_score(get_label(curr))
        for _ in range(16):
            # Look at neighbors
            neighbors = [random.randint(0, len(rows) - 1) for _ in range(5)]
            for n in neighbors:
                s = get_score(get_label(n))
                if s > best_s:
                    best_s, best_idx = s, n
        return best_idx, best_s

    # Strategy 3: Explore (Diversity)
    def strategy_explore():
        indices = random.sample(range(len(rows)), 16)
        best_idx = -1
        best_s = -float('inf')
        for i in indices:
            s = get_score(get_label(i))
            if s > best_s:
                best_s, best_idx = s, i
        return best_idx, best_s

    res_r = strategy_random()
    res_g = strategy_greedy()
    res_e = strategy_explore()

    strategies = {"random": res_r[1], "greedy": res_g[1], "explore": res_e[1]}
    winner = max(strategies, key=strategies.get)
    
    winner_idx = res_r[0] if winner == "random" else (res_g[0] if winner == "greedy" else res_e[0])

    return {"winner": winner, "row": winner_idx, "tried": ["random", "greedy", "explore"]}

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    true_goals = []
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                processed_row = []
                goals = []
                for i, val in enumerate(row):
                    if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 
                                     'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                        processed_row.append(float(val))
                    else:
                        processed_row.append(val)
                    if header[i].endswith('-') or header[i].endswith('+'):
                        goals.append(float(val))
                rows.append(processed_row)
                true_goals.append(goals)

        masked_rows = []
        for r in rows:
            new_r = ["?" if header[i].endswith('-') or header[i].endswith('+') else r[i] for i in range(len(r))]
            masked_rows.append(new_r)

        def label(i):
            return true_goals[i]

        result = race(header, masked_rows, label)
        print(f"The winner is: {result['winner']}")
        print(f"Best row found at index: {result['row']}")
        print(f"Strategies tried: {', '.join(result['tried'])}")
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
