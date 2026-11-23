import csv
import random
import step01
import step10

def race(header, rows, label):
    """
    Compares the customer's 'biggest team' strategy against random and 
    a simple hill-climber, sharing a 50-label budget.
    """
    budget = 50
    labeled = {}
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    team_size_idx = header.index('Team Size')

    def get_score(row):
        score = 0.0
        for idx, name in enumerate(header):
            if name.endswith('-'):
                score += row[idx]
            elif name.endswith('+'):
                score += (1.0 - row[idx])
        return score

    def get_true_row(i):
        if i not in labeled:
            if len(labeled) >= budget:
                return None
            true_vals = label(i)
            for j, g_idx in enumerate(goal_indices):
                rows[i][g_idx] = true_vals[j]
            labeled[i] = rows[i]
        return labeled[i]

    # Strategy 1: Random
    def strategy_random():
        best_idx, best_score = -1, float('inf')
        for _ in range(16):
            i = random.randint(0, len(rows) - 1)
            row = get_true_row(i)
            if row:
                s = get_score(row)
                if s < best_score: best_score, best_idx = s, i
        return best_idx, best_score

    # Strategy 2: Biggest Teams (Customer's current approach)
    def strategy_biggest():
        best_idx, best_score = -1, float('inf')
        # Sort by team size descending and pick top 17
        candidates = sorted(range(len(rows)), key=lambda i: rows[i][team_size_idx], reverse=True)
        for i in candidates[:17]:
            row = get_true_row(i)
            if row:
                s = get_score(row)
                if s < best_score: best_score, best_idx = s, i
        return best_idx, best_score

    # Strategy 3: Hill-Climber
    def strategy_hill():
        best_idx, best_score = -1, float('inf')
        curr = random.randint(0, len(rows) - 1)
        for _ in range(17):
            row = get_true_row(curr)
            if not row: break
            s = get_score(row)
            if s < best_score: best_score, best_idx = s, curr
            curr = (curr + random.randint(1, 10)) % len(rows)
        return best_idx, best_score

    results = {
        "random": strategy_random(),
        "biggest_teams": strategy_biggest(),
        "hill_climber": strategy_hill()
    }

    winner = min(results, key=lambda k: results[k][1])
    return {"winner": winner, "row": results[winner][0], "tried": list(results.keys())}

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rows.append([float(x) for x in row])

    true_data = [list(r) for r in rows]
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    
    for row in rows:
        for idx in goal_indices:
            row[idx] = "?"

    def label(i):
        return [true_data[i][idx] for idx in goal_indices]

    result = race(header, rows, label)
    print("Customer Inquiry: Is 'biggest teams' better than other search strategies?")
    print(f"Analysis: The '{result['winner']}' strategy performed best within our 50-label budget.")
    if result['winner'] == "biggest_teams":
        print("Result: Your current 'biggest teams' approach is optimal.")
    else:
        print(f"Result: No, the '{result['winner']}' strategy found a better configuration than 'biggest_teams'.")
