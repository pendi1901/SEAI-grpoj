import csv
import random

def race(header, rows, label):
    """
    Compares three strategies:
    1. 'random': Picks 16 random rows.
    2. 'biggest_teams': Picks 16 rows with the largest 'Team Size'.
    3. 'greedy': Picks 16 rows at random and selects the best.
    """
    goal_indices = [(i, name[-1]) for i, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+')]
    team_idx = header.index('Team Size')

    labeled = {}
    def get_label(i):
        if i not in labeled:
            if len(labeled) >= 50:
                raise Exception("Budget exceeded")
            labeled[i] = label(i)
        return labeled[i]

    def score_row(i):
        vals = get_label(i)
        total = 0.0
        for j, (idx, op) in enumerate(goal_indices):
            val = float(vals[j])
            total += val if op == '-' else (1.0 - val)
        return total

    # Strategy 1: Random
    def strategy_random():
        best_idx, best_score = -1, float('inf')
        for _ in range(16):
            i = random.randrange(len(rows))
            s = score_row(i)
            if s < best_score: best_score, best_idx = s, i
        return best_idx, best_score

    # Strategy 2: Biggest Teams (Customer's current approach)
    def strategy_biggest_teams():
        # Sort indices by Team Size descending
        sorted_indices = sorted(range(len(rows)), key=lambda i: float(rows[i][team_idx]), reverse=True)
        best_idx, best_score = -1, float('inf')
        for i in sorted_indices[:16]:
            s = score_row(i)
            if s < best_score: best_score, best_idx = s, i
        return best_idx, best_score

    # Strategy 3: Greedy (Sample 16, pick best)
    def strategy_greedy():
        indices = random.sample(range(len(rows)), 16)
        best_idx, best_score = -1, float('inf')
        for i in indices:
            s = score_row(i)
            if s < best_score: best_score, best_idx = s, i
        return best_idx, best_score

    results = {
        "random": strategy_random(),
        "biggest_teams": strategy_biggest_teams(),
        "greedy": strategy_greedy()
    }

    winner = min(results, key=lambda k: results[k][1])
    return {
        "winner": winner,
        "row": results[winner][0],
        "tried": ["random", "biggest_teams", "greedy"]
    }

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
            
            def label(i):
                return [float(rows[i][j]) for j, name in enumerate(header) 
                        if name.endswith('-') or name.endswith('+')]
            
            result = race(header, rows, label)
            
            print("Customer Inquiry: Is your way of choosing better than our 'biggest teams' approach?")
            print(f"Analysis: We compared 'random', 'greedy', and your 'biggest_teams' strategy.")
            print(f"The winning strategy was: {result['winner']}.")
            if result['winner'] == 'biggest_teams':
                print("Your current approach is optimal.")
            else:
                print(f"Our search found a better configuration at index {result['row']} using the {result['winner']} strategy.")
                
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
