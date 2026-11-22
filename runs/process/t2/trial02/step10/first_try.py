import csv
import random
from step01 import remember
from step07 import choose

def race(header, rows, label):
    """
    Compares three strategies: random, greedy (top 5% of training), and 
    a simple heuristic search. Total budget of 50 labels shared.
    """
    budget = 50
    labeled = {}

    def get_true_goals(i):
        if i not in labeled:
            if len(labeled) >= budget:
                raise Exception("Budget exceeded")
            labeled[i] = label(i)
        return labeled[i]

    def get_score(row_goals):
        s = 0
        for i, name in enumerate(header):
            if name.endswith('-'):
                s += float(row_goals[i])
            elif name.endswith('+'):
                s -= float(row_goals[i])
        return s

    # Strategy 1: Random
    def strategy_random():
        idx = random.randint(0, len(rows) - 1)
        return idx, get_score(get_true_goals(idx))

    # Strategy 2: Greedy (using remember logic)
    def strategy_greedy():
        # Use first 500 rows as training to pick a candidate
        best_indices = remember(header, rows[:500])
        idx = best_indices[0]
        return idx, get_score(get_true_goals(idx))

    # Strategy 3: Heuristic (sample 10 and pick best)
    def strategy_heuristic():
        indices = random.sample(range(len(rows)), 10)
        best_idx = -1
        best_s = float('inf')
        for i in indices:
            s = get_score(get_true_goals(i))
            if s < best_s:
                best_s = s
                best_idx = i
        return best_idx, best_s

    results = {}
    for name, func in [("random", strategy_random), 
                       ("greedy", strategy_greedy), 
                       ("heuristic", strategy_heuristic)]:
        idx, score = func()
        results[name] = (idx, score)

    winner = min(results, key=lambda n: results[n][1])
    return {
        "winner": winner,
        "row": results[winner][0],
        "tried": ["random", "greedy", "heuristic"]
    }

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]

        def label(i):
            return rows[i]

        outcome = race(header, rows, label)
        print(f"The winner is: {outcome['winner']}")
        print(f"Best row found at index: {outcome['row']}")
        print(f"Strategies tried: {', '.join(outcome['tried'])}")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
