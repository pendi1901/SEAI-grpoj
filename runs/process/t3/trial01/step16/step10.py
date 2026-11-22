import csv
import random

def race(header, rows, label):
    """
    Compares three strategies: random, greedy, and hill-climbing.
    Budget: 50 labels total.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    
    def get_score(goals):
        score = 0
        for i, g_idx in enumerate(goal_indices):
            val = goals[i]
            # Normalize: for '-', lower is better; for '+', higher is better
            # Since we don't have global range, we assume 0-1 range based on data
            if header[g_idx].endswith('-'):
                score += (1.0 - val)
            else:
                score += val
        return score / len(goal_indices)

    # Strategy 1: Random
    def strategy_random(budget):
        indices = random.sample(range(len(rows)), budget)
        best_idx, best_score = -1, -float('inf')
        for idx in indices:
            score = get_score(label(idx))
            if score > best_score:
                best_score, best_idx = score, idx
        return best_idx, best_score

    # Strategy 2: Greedy (Sample first 25, then pick best)
    def strategy_greedy(budget):
        indices = list(range(budget))
        best_idx, best_score = -1, -float('inf')
        for idx in indices:
            score = get_score(label(idx))
            if score > best_score:
                best_score, best_idx = score, idx
        return best_idx, best_score

    # Strategy 3: Hill Climbing (Start random, look at neighbors)
    def strategy_hill(budget):
        curr = random.randint(0, len(rows) - 1)
        best_idx, best_score = curr, get_score(label(curr))
        for _ in range(budget - 1):
            neighbor = random.randint(0, len(rows) - 1)
            score = get_score(label(neighbor))
            if score > best_score:
                best_score, best_idx = score, neighbor
        return best_idx, best_score

    # Allocate budget: 16 labels per strategy (48 total)
    strategies = {
        "random": lambda: strategy_random(16),
        "greedy": lambda: strategy_greedy(16),
        "hill": lambda: strategy_hill(16)
    }
    
    results = {}
    for name, func in strategies.items():
        results[name] = func()
        
    winner = max(results, key=lambda n: results[n][1])
    
    return {
        "winner": winner,
        "row": results[winner][0],
        "tried": list(strategies.keys())
    }

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            true_goals = []
            for row in reader:
                processed = []
                goals = []
                for i, val in enumerate(row):
                    if header[i].endswith(('-', '+')):
                        goals.append(float(val))
                        processed.append("?")
                    else:
                        processed.append(float(val))
                rows.append(processed)
                true_goals.append(goals)

        called = set()
        def label(i):
            if i not in called:
                if len(called) >= 50:
                    raise Exception("Budget exceeded")
                called.add(i)
            return true_goals[i]

        result = race(header, rows, label)
        print(f"Race Results:")
        print(f"Winner: {result['winner']}")
        print(f"Best Row Index Found: {result['row']}")
        print(f"Strategies Compared: {', '.join(result['tried'])}")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
