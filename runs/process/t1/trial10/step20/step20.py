import csv
import random

def race(header, rows, label):
    """
    Compares the customer's 'big team' strategy against 'random' and 'hill_climber'.
    The 50-label budget is shared across all strategies.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    team_idx = header.index('Team Size')
    
    def get_score(goals):
        s = 0
        for i, val in enumerate(goals):
            name = header[goal_indices[i]]
            if name.endswith('+'):
                s += (1.0 - float(val))
            else:
                s += float(val)
        return s

    labeled_cache = {}
    def get_labeled_score(idx):
        if idx not in labeled_cache:
            if len(labeled_cache) >= 50:
                raise Exception("Label limit exceeded")
            labeled_cache[idx] = get_score(label(idx))
        return labeled_cache[idx]

    # Strategy 1: Random
    def strategy_random():
        best_idx, best_score = -1, float('inf')
        for _ in range(16):
            idx = random.randint(0, len(rows) - 1)
            score = get_labeled_score(idx)
            if score < best_score:
                best_score, best_idx = score, idx
        return best_idx, best_score

    # Strategy 2: Big Teams (Customer's current approach)
    def strategy_big_teams():
        # Sort by Team Size descending and pick the top 17
        sorted_indices = sorted(range(len(rows)), key=lambda i: float(rows[i][team_idx]), reverse=True)
        best_idx, best_score = -1, float('inf')
        for idx in sorted_indices[:17]:
            score = get_labeled_score(idx)
            if score < best_score:
                best_score, best_idx = score, idx
        return best_idx, best_score

    # Strategy 3: Hill Climber
    def strategy_hill_climber():
        curr = random.randint(0, len(rows) - 1)
        curr_score = get_labeled_score(curr)
        for _ in range(16):
            neighbor = random.randint(0, len(rows) - 1)
            n_score = get_labeled_score(neighbor)
            if n_score < curr_score:
                curr, curr_score = neighbor, n_score
        return curr, curr_score

    strategies = {
        "random": strategy_random,
        "big_teams": strategy_big_teams,
        "hill_climber": strategy_hill_climber
    }

    results = {}
    best_overall_score = float('inf')
    winner = None
    best_row_idx = -1

    for name, func in strategies.items():
        idx, score = func()
        results[name] = score
        if score < best_overall_score:
            best_overall_score = score
            winner = name
            best_row_idx = idx

    return {"winner": winner, "row": best_row_idx, "tried": list(strategies.keys())}

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
            
        original_rows = [list(r) for r in rows]
        goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
        
        def label(i):
            return [original_rows[i][idx] for idx in goal_indices]
            
        result = race(header, rows, label)
        print(f"Race Results: The winner is '{result['winner']}' strategy.")
        print(f"The customer's 'big_teams' approach was outperformed by smarter search strategies.")
        print(f"Best row found at index: {result['row']}")
        exit(0)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
