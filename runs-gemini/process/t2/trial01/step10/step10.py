import csv
import random
from step01 import remember
from step07 import choose

def get_score(header, row):
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    is_max = [name.endswith('+') for name in header if name.endswith(('-', '+'))]
    s = 0
    for i, idx in enumerate(goal_indices):
        val = float(row[idx])
        s += val if is_max[i] else (1.0 - val)
    return s / len(goal_indices)

def race(header, rows, label):
    """
    Compares three strategies: random, greedy (first 50), and remember (top 5%).
    """
    n = len(rows)
    
    # Strategy 1: Random
    def strategy_random(label_func):
        indices = random.sample(range(n), 50)
        best_idx = -1
        best_score = -1.0
        for idx in indices:
            row = rows[idx][:]
            goals = label_func(idx)
            for i, g_idx in enumerate([i for i, name in enumerate(header) if name.endswith(('-', '+'))]):
                row[g_idx] = goals[i]
            score = get_score(header, row)
            if score > best_score:
                best_score, best_idx = score, idx
        return best_idx, best_score

    # Strategy 2: Greedy (First 50)
    def strategy_greedy(label_func):
        best_idx = -1
        best_score = -1.0
        for idx in range(50):
            row = rows[idx][:]
            goals = label_func(idx)
            for i, g_idx in enumerate([i for i, name in enumerate(header) if name.endswith(('-', '+'))]):
                row[g_idx] = goals[i]
            score = get_score(header, row)
            if score > best_score:
                best_score, best_idx = score, idx
        return best_idx, best_score

    # Strategy 3: Remember-based (Top 5% of first 1000)
    def strategy_remember(label_func):
        # Use first 1000 to find 'best' candidates, then sample 50
        sample_rows = rows[:1000]
        best_indices = remember(header, sample_rows)
        indices = best_indices[:50]
        best_idx = -1
        best_score = -1.0
        for idx in indices:
            row = rows[idx][:]
            goals = label_func(idx)
            for i, g_idx in enumerate([i for i, name in enumerate(header) if name.endswith(('-', '+'))]):
                row[g_idx] = goals[i]
            score = get_score(header, row)
            if score > best_score:
                best_score, best_idx = score, idx
        return best_idx, best_score

    strategies = {
        "random": strategy_random,
        "greedy": strategy_greedy,
        "remember": strategy_remember
    }
    
    results = {}
    best_overall_score = -1.0
    winner = ""
    best_row = -1
    
    for name, func in strategies.items():
        idx, score = func(label)
        results[name] = score
        if score > best_overall_score:
            best_overall_score = score
            winner = name
            best_row = idx
            
    return {"winner": winner, "row": best_row, "tried": list(strategies.keys())}

if __name__ == "__main__":
    filename = "pom3a.train.csv"
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [row for row in reader]
    
    true_data = [[float(row[i]) for i, name in enumerate(header) if name.endswith(('-', '+'))] for row in rows]
    def label(i): return true_data[i]
    
    result = race(header, rows, label)
    print(f"The winning strategy is: {result['winner']}")
    print(f"Best row found at index: {result['row']}")
    print(f"Strategies compared: {', '.join(result['tried'])}")
