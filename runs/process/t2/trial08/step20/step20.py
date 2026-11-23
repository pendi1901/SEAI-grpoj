import csv
import random as r
import step01

def race(header, rows, label):
    """
    Compares three strategies:
    1. 'random': Picks 16 random setups.
    2. 'big_teams': Picks 17 setups with the largest 'Team Size'.
    3. 'remember': Picks 17 setups and uses step01 logic to find the best.
    """
    budget = 50
    tried_indices = {}

    def get_score(row_with_goals):
        total = 0
        for i, name in enumerate(header):
            if name.endswith('-'):
                total += row_with_goals[i]
            elif name.endswith('+'):
                total += (1.0 - row_with_goals[i])
        return total

    def get_full_row(idx):
        if idx not in tried_indices:
            if len(tried_indices) >= budget:
                raise Exception("Budget exceeded")
            goals = label(idx)
            full_row = list(rows[idx])
            goal_idx = 0
            for i, name in enumerate(header):
                if name.endswith('-') or name.endswith('+'):
                    full_row[i] = goals[goal_idx]
                    goal_idx += 1
            tried_indices[idx] = full_row
        return tried_indices[idx]

    # Strategy 1: Random (16 trials)
    random_samples = r.sample(range(len(rows)), 16)
    best_random_idx = -1
    best_random_score = float('inf')
    for idx in random_samples:
        row = get_full_row(idx)
        score = get_score(row)
        if score < best_random_score:
            best_random_score = score
            best_random_idx = idx

    # Strategy 2: Big Teams (17 trials)
    team_idx = header.index('Team Size')
    # Sort by team size descending and pick top 17
    sorted_by_size = sorted(range(len(rows)), key=lambda i: rows[i][team_idx], reverse=True)
    big_team_samples = sorted_by_size[:17]
    best_big_idx = -1
    best_big_score = float('inf')
    for idx in big_team_samples:
        row = get_full_row(idx)
        score = get_score(row)
        if score < best_big_score:
            best_big_score = score
            best_big_idx = idx

    # Strategy 3: Remember (17 trials)
    rem_samples = r.sample(range(len(rows)), 17)
    rem_rows = [get_full_row(i) for i in rem_samples]
    best_rem_local_indices = step01.remember(header, rem_rows)
    best_rem_idx = rem_samples[best_rem_local_indices[0]]
    best_rem_score = get_score(rem_rows[best_rem_local_indices[0]])

    results = {
        "random": (best_random_score, best_random_idx),
        "big_teams": (best_big_score, best_big_idx),
        "remember": (best_rem_score, best_rem_idx)
    }

    winner = min(results, key=lambda k: results[k][0])
    
    return {
        "winner": winner,
        "row": results[winner][1],
        "tried": ["random", "big_teams", "remember"]
    }

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(x) for x in row] for row in reader]
        
        def label(i):
            return [rows[i][j] for j, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+')]
        
        result = race(header, rows, label)
        print("Customer Inquiry: Is your way of choosing any better than giving every programme the biggest teams?")
        print(f"Answer: The '{result['winner']}' strategy performed best. Your current 'big_teams' approach was compared against random and optimization strategies.")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
