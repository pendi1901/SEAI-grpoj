import csv
import random
from step01 import remember
from step07 import choose

def race(header, rows, label):
    """
    Compares three strategies: random, greedy (top-k), and a simple heuristic.
    Budget is 50 labels total.
    """
    budget = 50
    state = {'labeled': {}}

    def get_label(i):
        if i not in state['labeled']:
            if len(state['labeled']) >= budget:
                raise Exception("Budget exceeded")
            state['labeled'][i] = label(i)
        return state['labeled'][i]

    def get_score(row_idx):
        # Normalize goals for comparison
        goals = get_label(row_idx)
        goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
        goal_directions = [-1 if header[i].endswith('-') else 1 for i in goal_indices]
        
        # We need global min/max to normalize, but we only have 50 labels.
        # We use the 50 sampled rows as the population for normalization.
        sampled_indices = list(state['labeled'].keys())
        all_goals = [state['labeled'][idx] for idx in sampled_indices]
        
        scores = []
        for i, g_idx in enumerate(goal_indices):
            col_vals = [g[i] for g in all_goals]
            mn, mx = min(col_vals), max(col_vals)
            val = goals[i]
            norm = (val - mn) / (mx - mn) if mx > mn else 0
            scores.append(1 - norm if goal_directions[i] == -1 else norm)
        return min(scores)

    # Strategies
    def strategy_random():
        idx = random.choice(range(len(rows)))
        get_label(idx)
        return idx

    def strategy_greedy():
        # Sample 10, pick best, repeat
        best_idx = -1
        best_score = -1
        for _ in range(5):
            sample = random.sample(range(len(rows)), 10)
            for idx in sample:
                s = get_score(idx)
                if s > best_score:
                    best_score = s
                    best_idx = idx
        return best_idx

    def strategy_heuristic():
        # Pick rows with high 'Size' or 'Team Size' (common drivers)
        candidates = [i for i, r in enumerate(rows) if r[header.index('Size')] > 0.5]
        idx = random.choice(candidates) if candidates else random.choice(range(len(rows)))
        get_label(idx)
        return idx

    # Run strategies
    strategies = {"random": strategy_random, "greedy": strategy_greedy, "heuristic": strategy_heuristic}
    results = {}
    for name, func in strategies.items():
        try:
            results[name] = func()
        except:
            break

    # Determine winner
    best_strategy = max(results, key=lambda n: get_score(results[n]))
    
    return {
        "winner": best_strategy,
        "row": results[best_strategy],
        "tried": list(strategies.keys())
    }

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [[float(val) for val in row] for row in reader]

    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    
    def label(i):
        return [rows[i][idx] for idx in goal_indices]

    result = race(header, rows, label)
    print(f"Winner: {result['winner']}")
    print(f"Best row index found: {result['row']}")
    print(f"Strategies tried: {', '.join(result['tried'])}")
