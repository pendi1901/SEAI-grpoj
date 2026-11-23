import csv
import random

def race(header, rows, label):
    """
    Compares three strategies: random, greedy, and explorer.
    Budget: 50 labels total.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    is_min = [name.endswith('-') for name in header if name.endswith('-') or name.endswith('+')]

    def get_score(goal_values):
        total = 0
        for i, val in enumerate(goal_values):
            total += val if is_min[i] else (1.0 - val)
        return total

    # Shared budget
    budget = 50
    labeled = {}

    def get_labeled(idx):
        if idx not in labeled:
            labeled[idx] = label(idx)
        return labeled[idx]

    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), budget // 3)
        best_idx = -1
        best_score = float('inf')
        for idx in indices:
            score = get_score(get_labeled(idx))
            if score < best_score:
                best_score, best_idx = score, idx
        return best_idx, best_score

    # Strategy 2: Greedy (Sample first 10, then pick best neighbor)
    def strategy_greedy():
        current = random.randint(0, len(rows) - 1)
        for _ in range((budget // 3) - 1):
            neighbors = [random.randint(0, len(rows) - 1) for _ in range(5)]
            best_n = current
            best_s = get_score(get_labeled(current))
            for n in neighbors:
                s = get_score(get_labeled(n))
                if s < best_s:
                    best_s, best_n = s, n
            current = best_n
        return current, get_score(get_labeled(current))

    # Strategy 3: Explorer (Sample evenly)
    def strategy_explorer():
        indices = [int(i * (len(rows) - 1) / (budget // 3)) for i in range(budget // 3)]
        best_idx = -1
        best_score = float('inf')
        for idx in indices:
            score = get_score(get_labeled(idx))
            if score < best_score:
                best_score, best_idx = score, idx
        return best_idx, best_score

    strategies = {
        "random": strategy_random,
        "greedy": strategy_greedy,
        "explorer": strategy_explorer
    }

    results = {}
    for name, func in strategies.items():
        idx, score = func()
        results[name] = (idx, score)

    winner = min(results, key=lambda k: results[k][1])
    return {
        "winner": winner,
        "row": results[winner][0],
        "tried": list(strategies.keys())
    }

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            true_goals = []
            for row in reader:
                processed = []
                goals = []
                for i, val in enumerate(row):
                    if header[i].endswith('-') or header[i].endswith('+'):
                        goals.append(float(val))
                        processed.append("?")
                    else:
                        processed.append(float(val))
                rows.append(processed)
                true_goals.append(goals)

        def label(i):
            return true_goals[i]

        result = race(header, rows, label)
        print(f"Race Results:")
        print(f"  Winner: {result['winner']}")
        print(f"  Best Row Index: {result['row']}")
        print(f"  Strategies tried: {', '.join(result['tried'])}")
        exit(0)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
