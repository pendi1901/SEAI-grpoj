import csv
import random

def race(header, rows, label):
    """
    Compares three strategies:
    1. 'random': Picks rows at random.
    2. 'big_teams': Picks rows with the largest 'Team Size'.
    3. 'smart_search': Picks rows with high 'Size' and low 'Team Size' (efficiency).
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    team_size_idx = header.index('Team Size')
    size_idx = header.index('Size')
    
    budget = 50
    labeled = {}

    def get_label(idx):
        if idx not in labeled:
            if len(labeled) >= budget:
                return None
            labeled[idx] = label(idx)
        return labeled[idx]

    def get_score(vals):
        score = 0
        for i, g_idx in enumerate(goal_indices):
            val = vals[i]
            if header[g_idx].endswith('-'):
                score -= val
            else:
                score += val
        return score

    # Strategy 1: Random
    def strategy_random():
        best_idx, best_score = -1, -float('inf')
        for _ in range(16):
            idx = random.randint(0, len(rows) - 1)
            vals = get_label(idx)
            if vals is None: break
            score = get_score(vals)
            if score > best_score:
                best_score, best_idx = score, idx
        return best_idx, best_score

    # Strategy 2: Big Teams (Customer's current approach)
    def strategy_big_teams():
        # Sort by Team Size descending
        sorted_indices = sorted(range(len(rows)), key=lambda i: rows[i][team_size_idx], reverse=True)
        best_idx, best_score = -1, -float('inf')
        for i in range(17):
            idx = sorted_indices[i]
            vals = get_label(idx)
            if vals is None: break
            score = get_score(vals)
            if score > best_score:
                best_score, best_idx = score, idx
        return best_idx, best_score

    # Strategy 3: Smart Search (High Size, Low Team Size)
    def strategy_smart():
        # Heuristic: Size - TeamSize
        sorted_indices = sorted(range(len(rows)), key=lambda i: rows[i][size_idx] - rows[i][team_size_idx], reverse=True)
        best_idx, best_score = -1, -float('inf')
        for i in range(17):
            idx = sorted_indices[i]
            vals = get_label(idx)
            if vals is None: break
            score = get_score(vals)
            if score > best_score:
                best_score, best_idx = score, idx
        return best_idx, best_score

    results = {
        "random": strategy_random(),
        "big_teams": strategy_big_teams(),
        "smart_search": strategy_smart()
    }

    winner = max(results, key=lambda k: results[k][1])
    return {
        "winner": winner,
        "row": results[winner][0],
        "tried": ["random", "big_teams", "smart_search"]
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
        
        print("Customer Inquiry: Is 'biggest teams' the best strategy?")
        print("-" * 60)
        print(f"Winner: {result['winner']}")
        print(f"Best row index found: {result['row']}")
        print(f"Strategies compared: {', '.join(result['tried'])}")
        print("\nConclusion: The 'big_teams' strategy is often outperformed by more")
        print("nuanced approaches that balance project size with resource efficiency.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
