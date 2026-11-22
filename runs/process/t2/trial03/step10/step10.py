import csv
import random
import step01
import step07

def race(header, rows, label):
    """
    Compares three strategies: random, greedy (best of sample), 
    and a local search variant.
    """
    goal_indices = [i for i, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+')]

    def get_score(row):
        total = 0.0
        for idx in goal_indices:
            val = float(row[idx])
            if header[idx].endswith('-'):
                total += val
            else:
                total += (1.0 - val)
        return total

    budget = 50
    labeled = {}

    def get_labeled_row(i):
        if i not in labeled:
            if len(labeled) >= budget:
                raise Exception("Budget exceeded")
            goals = label(i)
            row = list(rows[i])
            for g_idx, val in zip(goal_indices, goals):
                row[g_idx] = val
            labeled[i] = row
        return labeled[i]

    # Strategy 1: Random
    def strategy_random():
        idx = random.choice(range(len(rows)))
        return idx, get_score(get_labeled_row(idx))

    # Strategy 2: Greedy (Sample 20)
    def strategy_greedy():
        samples = random.sample(range(len(rows)), 20)
        best_idx = -1
        best_s = float('inf')
        for i in samples:
            s = get_score(get_labeled_row(i))
            if s < best_s:
                best_s = s
                best_idx = i
        return best_idx, best_s

    # Strategy 3: Hill-Climb (Sample 10, then 10 neighbors)
    def strategy_hill():
        curr = random.choice(range(len(rows)))
        best_s = get_score(get_labeled_row(curr))
        for _ in range(29): # Remaining budget
            neighbor = random.choice(range(len(rows)))
            s = get_score(get_labeled_row(neighbor))
            if s < best_s:
                best_s = s
                curr = neighbor
        return curr, best_s

    results = {}
    for name, func in [("random", strategy_random), ("greedy", strategy_greedy), ("hill", strategy_hill)]:
        idx, score = func()
        results[name] = {"idx": idx, "score": score}

    winner = min(results, key=lambda n: results[n]["score"])
    return {"winner": winner, "row": results[winner]["idx"], "tried": ["random", "greedy", "hill"]}

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', newline='') as f:
            reader = csv.reader(f)
            header = next(reader)
            full_data = []
            for row in reader:
                full_data.append([float(val) if val.replace('.','',1).isdigit() or '-' in val else val for val in row])
        
        rows = [[val if not (header[i].endswith(('-', '+'))) else "?" for i, val in enumerate(r)] for r in full_data]
        
        def label(i):
            return [full_data[i][idx] for idx, name in enumerate(header) if name.endswith(('-', '+'))]
        
        res = race(header, rows, label)
        print(f"Race results: The winner is '{res['winner']}' strategy.")
        print(f"Best row found at index: {res['row']}")
        print(f"Strategies compared: {', '.join(res['tried'])}")
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
