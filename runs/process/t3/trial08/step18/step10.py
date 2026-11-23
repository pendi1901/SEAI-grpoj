import csv
import random

def race(header, rows, label):
    """
    Compares three strategies: random, greedy (hill climbing), and 
    a simple heuristic-based search.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    
    def get_score(row_vals):
        score = 0
        for i, g_idx in enumerate(goal_indices):
            val = row_vals[i]
            if header[g_idx].endswith('-'):
                score -= val
            else:
                score += val
        return score

    budget = 50
    labeled = {}

    def get_label(idx):
        if idx not in labeled:
            if len(labeled) >= budget:
                return None
            labeled[idx] = label(idx)
        return labeled[idx]

    # Strategy 1: Random
    def strategy_random():
        best_idx = -1
        best_score = -float('inf')
        for _ in range(16): # 16 trials
            idx = random.randint(0, len(rows) - 1)
            vals = get_label(idx)
            if vals is None: break
            score = get_score(vals)
            if score > best_score:
                best_score, best_idx = score, idx
        return best_idx, best_score

    # Strategy 2: Greedy (Hill Climbing)
    def strategy_greedy():
        curr = random.randint(0, len(rows) - 1)
        best_idx, best_score = curr, get_score(get_label(curr))
        for _ in range(16): # 16 trials
            neighbor = random.randint(0, len(rows) - 1)
            vals = get_label(neighbor)
            if vals is None: break
            score = get_score(vals)
            if score > best_score:
                best_score, best_idx = score, neighbor
        return best_idx, best_score

    # Strategy 3: Heuristic (Focus on low 'Cost-' and 'Idle-')
    def strategy_heuristic():
        best_idx, best_score = -1, -float('inf')
        for _ in range(17): # 17 trials
            idx = random.randint(0, len(rows) - 1)
            vals = get_label(idx)
            if vals is None: break
            # Heuristic: prioritize rows with low Cost- (index 9)
            score = -vals[0] 
            if score > best_score:
                best_score, best_idx = score, idx
        return best_idx, best_score

    results = {
        "random": strategy_random(),
        "greedy": strategy_greedy(),
        "heuristic": strategy_heuristic()
    }

    winner = max(results, key=lambda k: results[k][1])
    return {
        "winner": winner,
        "row": results[winner][0],
        "tried": ["random", "greedy", "heuristic"]
    }

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) if header[i][0].isupper() else val for i, val in enumerate(row)])
        
        def label(i):
            return [rows[i][j] for j, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
        
        result = race(header, rows, label)
        print(f"Race Results:")
        print(f"Winner: {result['winner']}")
        print(f"Best row index found: {result['row']}")
        print(f"Strategies compared: {', '.join(result['tried'])}")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
