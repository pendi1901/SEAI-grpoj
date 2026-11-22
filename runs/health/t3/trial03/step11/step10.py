import csv
import random

def race(header, rows, label):
    """
    Compares three strategies:
    1. 'random': Picks 16 random rows.
    2. 'greedy': Picks 17 rows by sampling, then greedily exploring neighbors.
    3. 'smart': Picks 17 rows by sampling, then focusing on the best-performing region.
    Total labels: 16 + 17 + 17 = 50.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    
    def get_score(goals):
        score = 0
        for i, val in enumerate(goals):
            direction = -1 if header[goal_indices[i]].endswith('-') else 1
            score += val * direction
        return score

    results = {}
    
    # Strategy 1: Random
    random_indices = random.sample(range(len(rows)), 16)
    best_r = -1
    best_s = float('-inf')
    for i in random_indices:
        s = get_score(label(i))
        if s > best_s:
            best_s, best_r = s, i
    results["random"] = (best_r, best_s)

    # Strategy 2: Greedy (Sample 10, then pick 7 neighbors of the best)
    sample_indices = random.sample(range(len(rows)), 10)
    best_g = -1
    best_s = float('-inf')
    for i in sample_indices:
        s = get_score(label(i))
        if s > best_s:
            best_s, best_g = s, i
    # Look for rows with similar N_estimators (index 3)
    for i in range(len(rows)):
        if len(results.get("greedy_tried", [])) >= 7: break
        if abs(rows[i][3] - rows[best_g][3]) < 10:
            s = get_score(label(i))
            if s > best_s:
                best_s, best_g = s, i
    results["greedy"] = (best_g, best_s)

    # Strategy 3: Smart (Sample 17, focusing on high N_estimators)
    smart_indices = [i for i in range(len(rows)) if rows[i][3] > 150]
    sample_smart = random.sample(smart_indices, min(17, len(smart_indices)))
    best_sm = -1
    best_s = float('-inf')
    for i in sample_smart:
        s = get_score(label(i))
        if s > best_s:
            best_s, best_sm = s, i
    results["smart"] = (best_sm, best_s)

    # Determine winner
    winner = max(results, key=lambda k: results[k][1])
    return {"winner": winner, "row": results[winner][0], "tried": ["random", "greedy", "smart"]}

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    header = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = [float(val) if val.replace('.', '', 1).isdigit() or (val.startswith('-') and val[1:].replace('.', '', 1).isdigit()) else val for val in row]
            rows.append(processed)

    true_goals = [[row[i] for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')] for row in rows]
    for row in rows:
        for i in range(len(row)):
            if header[i].endswith('-') or header[i].endswith('+'):
                row[i] = "?"

    labeled = set()
    def label(i):
        if i not in labeled:
            if len(labeled) >= 50: raise ValueError("Budget exceeded")
            labeled.add(i)
        return true_goals[i]

    outcome = race(header, rows, label)
    print(f"Winner: {outcome['winner']}")
    print(f"Best row found at index: {outcome['row']}")
    print(f"Strategies tried: {', '.join(outcome['tried'])}")
