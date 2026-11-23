import csv
import random

def get_score(header, row):
    """Calculates a normalized score [0, 1] for a row based on goals."""
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    scores = []
    for i in goal_indices:
        val = row[i]
        # Since data is normalized [0,1], we treat 1 as best
        if header[i].endswith('-'):
            scores.append(1.0 - val)
        else:
            scores.append(val)
    return sum(scores) / len(scores)

def race(header, rows, label):
    """
    Compares three strategies:
    1. 'random': Picks 16 random rows.
    2. 'biggest_teams': Picks 17 rows with the largest 'Team Size'.
    3. 'smart_search': Picks 17 rows that balance 'Team Size' and 'Size'.
    """
    budget = 50
    tried = ["random", "biggest_teams", "smart_search"]
    results = {}
    
    def get_full_row(idx):
        row = list(rows[idx])
        goals = label(idx)
        goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
        for i, g in zip(goal_indices, goals):
            row[i] = g
        return row

    # 1. Random Strategy
    random_indices = random.sample(range(len(rows)), 16)
    best_r_idx = -1
    best_r_score = -1.0
    for idx in random_indices:
        score = get_score(header, get_full_row(idx))
        if score > best_r_score:
            best_r_score = score
            best_r_idx = idx
    results["random"] = (best_r_score, best_r_idx)

    # 2. Biggest Teams Strategy (Customer's current approach)
    team_size_idx = header.index('Team Size')
    sorted_by_team = sorted(range(len(rows)), key=lambda i: rows[i][team_size_idx], reverse=True)
    best_b_idx = -1
    best_b_score = -1.0
    for idx in sorted_by_team[:17]:
        score = get_score(header, get_full_row(idx))
        if score > best_b_score:
            best_b_score = score
            best_b_idx = idx
    results["biggest_teams"] = (best_b_score, best_b_idx)

    # 3. Smart Search (Balanced approach)
    # Pick rows with moderate team size and high project size
    size_idx = header.index('Size')
    smart_indices = sorted(range(len(rows)), key=lambda i: (rows[i][size_idx] - rows[i][team_size_idx]), reverse=True)
    best_s_idx = -1
    best_s_score = -1.0
    for idx in smart_indices[:17]:
        score = get_score(header, get_full_row(idx))
        if score > best_s_score:
            best_s_score = score
            best_s_idx = idx
    results["smart_search"] = (best_s_score, best_s_idx)

    winner = max(results, key=lambda k: results[k][0])
    return {"winner": winner, "row": results[winner][1], "tried": tried}

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(x) if i < 9 else float(x) for i, x in enumerate(row)])
        
        def label(i):
            return [rows[i][j] for j, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
        
        result = race(header, rows, label)
        
        print("Customer Report: Optimization Strategy Comparison")
        print(f"The winning strategy is: {result['winner']}")
        print(f"Best setup found at index: {result['row']}")
        
        if result['winner'] == "biggest_teams":
            print("Your current strategy of using the biggest teams is optimal.")
        else:
            print(f"Your current strategy ('biggest_teams') was outperformed by '{result['winner']}'.")
            print("We recommend adopting a more balanced approach to resource allocation.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
