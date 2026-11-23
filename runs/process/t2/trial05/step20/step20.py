import csv
import random

def race(header, rows, label):
    """
    Compares three strategies:
    1. 'random': Picks 16 random rows.
    2. 'biggest_team': Picks 17 rows with the largest 'Team Size'.
    3. 'greedy': Picks 17 rows evenly spaced across the dataset.
    """
    goal_indices = [i for i, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+')]
    team_idx = header.index('Team Size')
    
    def get_score(row_vals):
        total = 0
        for i, g_idx in enumerate(goal_indices):
            val = float(row_vals[i])
            total += (1.0 - val) if header[g_idx].endswith('-') else val
        return total

    budget = 50
    labeled = {}

    def get_label(idx):
        if idx not in labeled:
            if len(labeled) >= budget:
                raise Exception("Budget exceeded")
            labeled[idx] = label(idx)
        return labeled[idx]

    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), 16)
        best_idx, best_score = -1, -1.0
        for idx in indices:
            score = get_score(get_label(idx))
            if score > best_score:
                best_score, best_idx = score, idx
        return best_idx, best_score

    # Strategy 2: Biggest Team (Customer's current approach)
    def strategy_biggest():
        # Sort indices by Team Size descending
        sorted_indices = sorted(range(len(rows)), key=lambda i: rows[i][team_idx], reverse=True)
        best_idx, best_score = -1, -1.0
        for idx in sorted_indices[:17]:
            score = get_score(get_label(idx))
            if score > best_score:
                best_score, best_idx = score, idx
        return best_idx, best_score

    # Strategy 3: Greedy (Evenly spaced)
    def strategy_greedy():
        indices = [int(i * (len(rows) - 1) / 16) for i in range(17)]
        best_idx, best_score = -1, -1.0
        for idx in indices:
            score = get_score(get_label(idx))
            if score > best_score:
                best_score, best_idx = score, idx
        return best_idx, best_score

    strategies = {
        "random": strategy_random,
        "biggest_team": strategy_biggest,
        "greedy": strategy_greedy
    }

    results = {}
    for name, func in strategies.items():
        idx, score = func()
        results[name] = (idx, score)

    winner = max(results, key=lambda k: results[k][1])
    
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
            for row in reader:
                rows.append([float(val) for val in row])
        
        def label(i):
            return [rows[i][col] for col, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+')]
        
        outcome = race(header, rows, label)
        print(f"Comparison Result: The winning strategy is '{outcome['winner']}'.")
        if outcome['winner'] == "biggest_team":
            print("Your current strategy of using the biggest teams is optimal.")
        else:
            print(f"Your current strategy was outperformed by '{outcome['winner']}'.")
        print(f"Strategies compared: {', '.join(outcome['tried'])}")
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
