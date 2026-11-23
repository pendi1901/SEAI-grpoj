import csv
import random

def race(header, rows, label):
    """
    Compares three strategies:
    1. 'random': Picks rows at random.
    2. 'biggest_teams': The customer's current strategy (picks rows with largest Team Size).
    3. 'greedy': Picks a random sample, then explores the neighborhood of the best.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    team_size_idx = header.index('Team Size')
    
    # Shared budget
    budget = 50
    tried_indices = {}

    def get_score(row_goals):
        s = 0
        for i, val in enumerate(row_goals):
            idx = goal_indices[i]
            s += val if header[idx].endswith('-') else (1.0 - val)
        return s

    def get_label(i):
        if i not in tried_indices:
            if len(tried_indices) >= budget:
                raise Exception("Exceeded 50 labels!")
            tried_indices[i] = get_score(label(i))
        return tried_indices[i]

    # Strategy 1: Random
    def strategy_random():
        best_idx = -1
        best_score = float('inf')
        for _ in range(16):
            idx = random.randint(0, len(rows) - 1)
            score = get_label(idx)
            if score < best_score:
                best_score, best_idx = score, idx
        return best_idx, best_score

    # Strategy 2: Biggest Teams (Customer's current way)
    def strategy_biggest_teams():
        # Sort indices by Team Size descending
        sorted_indices = sorted(range(len(rows)), key=lambda i: rows[i][team_size_idx], reverse=True)
        best_idx = -1
        best_score = float('inf')
        # Check top 16 biggest teams
        for i in sorted_indices[:16]:
            score = get_label(i)
            if score < best_score:
                best_score, best_idx = score, i
        return best_idx, best_score

    # Strategy 3: Greedy (Sample 10, then explore neighbors)
    def strategy_greedy():
        samples = random.sample(range(len(rows)), 10)
        best_idx = min(samples, key=get_label)
        best_score = get_label(best_idx)
        # Explore 8 neighbors
        others = sorted(range(len(rows)), key=lambda i: sum((rows[i][j] - rows[best_idx][j])**2 for j in range(len(header)) if j not in goal_indices))
        for i in others[1:9]:
            score = get_label(i)
            if score < best_score:
                best_score, best_idx = score, i
        return best_idx, best_score

    results = {
        "random": strategy_random(),
        "biggest_teams": strategy_biggest_teams(),
        "greedy": strategy_greedy()
    }

    winner = min(results, key=lambda k: results[k][1])
    return {"winner": winner, "row": results[winner][0], "tried": list(results.keys())}

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        rows = []
        true_goals = []
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
            for row in reader:
                processed = []
                goals = []
                for i, val in enumerate(row):
                    if i in goal_indices:
                        goals.append(float(val))
                        processed.append("?")
                    else:
                        processed.append(float(val))
                rows.append(processed)
                true_goals.append(goals)

        def label(i): return true_goals[i]
        
        res = race(header, rows, label)
        print(f"Winner: {res['winner']}")
        print(f"Best row index found: {res['row']}")
        print(f"Strategies compared: {', '.join(res['tried'])}")
        if res['winner'] != "biggest_teams":
            print("Conclusion: Your current 'biggest teams' strategy is outperformed by smarter search methods.")
        else:
            print("Conclusion: Your current strategy is effective.")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
