import csv
import random

def get_score(header, row_goals):
    """Calculates a normalized score for a row's goals."""
    score = 0
    for i, val in enumerate(row_goals):
        if header[i].endswith('-'):
            score += (1 - val)
        else:
            score += val
    return score / len(row_goals)

def race(header, rows, label):
    """
    Compares three strategies: random, big_teams, and hill_climbing.
    Budget: 50 labels total.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    goal_headers = [header[i] for i in goal_indices]
    team_size_idx = header.index('Team Size')
    
    labeled = {}
    def get_labeled(i):
        if i not in labeled:
            if len(labeled) >= 50:
                raise Exception("Budget exceeded")
            labeled[i] = label(i)
        return labeled[i]

    # Strategy 1: Random (16 samples)
    def strategy_random():
        indices = random.sample(range(len(rows)), 16)
        best_idx, best_s = -1, -1
        for idx in indices:
            s = get_score(goal_headers, get_labeled(idx))
            if s > best_s:
                best_s, best_idx = s, idx
        return best_idx, best_s

    # Strategy 2: Big Teams (Customer's current approach: 16 samples with largest team sizes)
    def strategy_big_teams():
        # Sort indices by team size descending
        sorted_indices = sorted(range(len(rows)), key=lambda i: rows[i][team_size_idx], reverse=True)
        best_idx, best_s = -1, -1
        for idx in sorted_indices[:16]:
            s = get_score(goal_headers, get_labeled(idx))
            if s > best_s:
                best_s, best_idx = s, idx
        return best_idx, best_s

    # Strategy 3: Hill Climbing (18 samples)
    def strategy_hill():
        curr = random.randint(0, len(rows) - 1)
        best_idx, best_s = curr, get_score(goal_headers, get_labeled(curr))
        for _ in range(17):
            n = random.randint(0, len(rows) - 1)
            s = get_score(goal_headers, get_labeled(n))
            if s > best_s:
                best_s, best_idx = s, n
        return best_idx, best_s

    strategies = {"random": strategy_random, "big_teams": strategy_big_teams, "hill": strategy_hill}
    results = {}
    for name, func in strategies.items():
        idx, score = func()
        results[name] = {"idx": idx, "score": score}

    winner = max(results, key=lambda n: results[n]["score"])
    return {"winner": winner, "row": results[winner]["idx"], "tried": list(strategies.keys())}

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) if i < len(header) - 3 or (i >= len(header) - 3 and val.replace('.','',1).isdigit()) else val for i, val in enumerate(row)])
        
        def label(i):
            goal_indices = [j for j, h in enumerate(header) if h.endswith(('-', '+'))]
            return [rows[i][j] for j in goal_indices]

        result = race(header, rows, label)
        
        print("Customer Inquiry: Is 'biggest teams' better than our optimization?")
        print("-" * 70)
        print(f"Winner: {result['winner']}")
        print(f"Best Row Found: {result['row']}")
        print(f"Strategies Tried: {', '.join(result['tried'])}")
        
        if result['winner'] == 'big_teams':
            print("\nConclusion: Your current strategy of maximizing team size is optimal.")
        else:
            print(f"\nConclusion: No, the '{result['winner']}' strategy outperformed your current approach.")
            
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
