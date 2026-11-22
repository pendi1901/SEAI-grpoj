import csv
import random
from step01 import remember

def race(header, rows, label):
    """
    Compares three strategies: random, greedy, and heuristic.
    Total budget of 50 labels shared.
    """
    budget = 50
    labeled = {}

    def get_true_goals(i):
        if i not in labeled:
            if len(labeled) >= budget:
                raise Exception("Budget exceeded")
            labeled[i] = label(i)
        return labeled[i]

    def get_score(i):
        row_goals = get_true_goals(i)
        s = 0
        goal_names = [name for name in header if name.endswith('-') or name.endswith('+')]
        for name in goal_names:
            idx = header.index(name)
            val = float(row_goals[idx])
            s += val if name.endswith('-') else -val
        return s

    # Strategy 1: Random
    def strategy_random():
        idx = random.randint(0, len(rows) - 1)
        return idx, get_score(idx)

    # Strategy 2: Greedy (uses remember logic on first half of data)
    def strategy_greedy():
        best_indices = remember(header, rows[:len(rows)//2])
        idx = best_indices[0]
        return idx, get_score(idx)

    # Strategy 3: Heuristic (sample 10 random and pick best)
    def strategy_heuristic():
        indices = random.sample(range(len(rows)), 10)
        best_idx = indices[0]
        best_s = get_score(best_idx)
        for i in indices[1:]:
            s = get_score(i)
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
