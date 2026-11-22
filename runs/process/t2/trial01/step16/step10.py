import csv
import random
from step01 import remember

def race(header, rows, label):
    """
    Compares three strategies: random, greedy (based on first 10% sample), 
    and a heuristic search (best-so-far).
    """
    budget = 50
    labeled = {}

    def get_score(row_idx):
        if row_idx not in labeled:
            if len(labeled) >= budget:
                raise Exception("Label budget exceeded")
            labeled[row_idx] = label(row_idx)
        
        vals = labeled[row_idx]
        score = 0
        for i, name in enumerate(header):
            if name.endswith('-') or name.endswith('+'):
                # Find index in the goal list returned by label
                goal_idx = [j for j, n in enumerate(header) if n.endswith('-') or n.endswith('+')].index(i)
                val = vals[goal_idx]
                score += val if name.endswith('-') else (1.0 - val)
        return score

    # Strategy 1: Random
    def strategy_random():
        best_idx = -1
        best_score = float('inf')
        for _ in range(16): # 16 labels
            idx = random.randint(0, len(rows) - 1)
            score = get_score(idx)
            if score < best_score:
                best_score, best_idx = score, idx
        return best_idx, best_score

    # Strategy 2: Greedy (Sample first 10%, pick best)
    def strategy_greedy():
        sample_size = 17 # 17 labels
        best_idx = -1
        best_score = float('inf')
        for idx in range(sample_size):
            score = get_score(idx)
            if score < best_score:
                best_score, best_idx = score, idx
        return best_idx, best_score

    # Strategy 3: Hill-Climbing (Start random, look for neighbors)
    def strategy_hill():
        curr = random.randint(0, len(rows) - 1)
        curr_score = get_score(curr)
        for _ in range(16): # 17 labels total
            neighbor = random.randint(0, len(rows) - 1)
            n_score = get_score(neighbor)
            if n_score < curr_score:
                curr, curr_score = neighbor, n_score
        return curr, curr_score

    results = {
        "random": strategy_random(),
        "greedy": strategy_greedy(),
        "hill": strategy_hill()
    }

    winner = min(results, key=lambda k: results[k][1])
    return {
        "winner": winner,
        "row": results[winner][0],
        "tried": list(results.keys())
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
                processed = [float(val) if val.replace('.', '', 1).isdigit() or (val.startswith('-') and val[1:].replace('.', '', 1).isdigit()) else val for val in row]
                rows.append(processed)
                true_goals.append([float(row[i]) for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')])
        
        masked_rows = [["?" for _ in row] for row in rows]
        
        def label(i):
            return true_goals[i]

        result = race(header, masked_rows, label)
        print(f"Race Results:")
        print(f"Winner: {result['winner']}")
        print(f"Best row found at index: {result['row']}")
        print(f"Strategies compared: {', '.join(result['tried'])}")
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
