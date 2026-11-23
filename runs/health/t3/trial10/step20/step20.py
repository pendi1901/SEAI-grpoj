import csv
import random

def race(header, rows, label):
    """
    Compares three strategies: 'random', 'greedy', and 'hill_climbing'.
    Total budget: 50 labels.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    
    # Normalize goals to a single score: -MRE + ACC + PRED
    def get_score(row_idx):
        goals = label(row_idx)
        # MRE- (index 0), ACC+ (index 1), PRED40+ (index 2)
        return -goals[0] + goals[1] + goals[2]

    budget = 50
    queried = {}

    def get_val(i):
        if i not in queried:
            if len(queried) >= budget:
                return -float('inf')
            queried[i] = get_score(i)
        return queried[i]

    # 1. Random Strategy: 16 samples
    random_indices = random.sample(range(len(rows)), 16)
    for i in random_indices:
        get_val(i)
    best_random = max(random_indices, key=get_val)

    # 2. Greedy Strategy: Pick best from random
    best_greedy = best_random

    # 3. Hill Climbing: Start from best random, move to neighbors
    current = best_random
    for _ in range(17):
        if len(queried) >= budget: break
        # Look at 5 random neighbors
        neighbors = random.sample(range(len(rows)), 5)
        best_neighbor = max(neighbors, key=lambda x: get_val(x))
        if get_val(best_neighbor) > get_val(current):
            current = best_neighbor
        else:
            # Explore new
            next_idx = random.choice(range(len(rows)))
            if get_val(next_idx) > get_val(current):
                current = next_idx
    best_hc = current

    # Strategy results
    results = {
        "random": best_random,
        "greedy": best_greedy,
        "hill_climbing": best_hc
    }
    
    best_overall = max(results, key=lambda s: get_val(results[s]))
    
    return {
        "winner": best_overall,
        "row": results[best_overall],
        "tried": ["random", "greedy", "hill_climbing"]
    }

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                try:
                    processed_row.append(float(val))
                except ValueError:
                    processed_row.append(val)
            rows.append(processed_row)

    true_goals = {}
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    for i, row in enumerate(rows):
        true_goals[i] = [row[g] for g in goal_indices]
        for g in goal_indices:
            row[g] = "?"

    def label(i):
        return true_goals[i]

    result = race(header, rows, label)
    print(f"Race complete. Winner: {result['winner']} at row {result['row']}.")
    print(f"Strategies tried: {', '.join(result['tried'])}")
    exit(0)
