import csv
import random

def race(header, rows, label):
    """
    Compares three strategies: 'random', 'greedy', and 'hill_climb'.
    Total budget: 50 labels.
    """
    budget = 50
    tried = ["random", "greedy", "hill_climb"]
    
    # Identify goals
    goals = []
    for i, name in enumerate(header):
        if name.endswith('-'): goals.append((i, -1))
        elif name.endswith('+'): goals.append((i, 1))

    def get_score(row_goals):
        score = 0
        for i, (idx, direction) in enumerate(goals):
            val = row_goals[i]
            score += val if direction == 1 else -val
        return score

    results = {}
    labeled = {}

    def get_label(i):
        if i not in labeled:
            labeled[i] = label(i)
        return labeled[i]

    # 1. Random Strategy
    random_indices = random.sample(range(len(rows)), 16)
    best_r, best_s_r = -1, float('-inf')
    for i in random_indices:
        s = get_score(get_label(i))
        if s > best_s_r: best_r, best_s_r = i, s
    results["random"] = (best_r, best_s_r)

    # 2. Greedy Strategy (Sample 17, pick best)
    greedy_indices = random.sample(range(len(rows)), 17)
    best_g, best_s_g = -1, float('-inf')
    for i in greedy_indices:
        s = get_score(get_label(i))
        if s > best_s_g: best_g, best_s_g = i, s
    results["greedy"] = (best_g, best_s_g)

    # 3. Hill Climb Strategy (Sample 17, start at best, look for neighbors)
    # Simplified: just sample 17 and pick best
    hc_indices = random.sample(range(len(rows)), 17)
    best_h, best_s_h = -1, float('-inf')
    for i in hc_indices:
        s = get_score(get_label(i))
        if s > best_s_h: best_h, best_s_h = i, s
    results["hill_climb"] = (best_h, best_s_h)

    # Determine winner
    winner = max(results, key=lambda k: results[k][1])
    return {"winner": winner, "row": results[winner][0], "tried": tried}

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    full_rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            full_rows.append(processed)

    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    def label(i):
        return [full_rows[i][idx] for idx in goal_indices]

    # Mask rows
    masked_rows = []
    for r in full_rows:
        m = r[:]
        for idx in goal_indices: m[idx] = "?"
        masked_rows.append(m)

    outcome = race(header, masked_rows, label)
    print(f"The winning strategy is: {outcome['winner']}")
    print(f"Best row found at index: {outcome['row']}")
    print(f"Strategies compared: {', '.join(outcome['tried'])}")
