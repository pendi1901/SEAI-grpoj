import csv
import random

def get_score(header, goals):
    """Calculates a normalized score: 0 is best, 1 is worst."""
    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    score = 0.0
    for i, g_idx in enumerate(goal_indices):
        val = goals[i]
        if header[g_idx].endswith('-'):
            score += val
        else:
            score += (1.0 - val)
    return score / len(goal_indices)

def race(header, rows, label):
    """
    Compares three strategies:
    1. random: Picks 50 random rows.
    2. greedy: Picks 1, then 49 neighbors of the best found so far.
    3. explore: Picks 25 random, then 25 neighbors of the best found.
    """
    tried = ["random", "greedy", "explore"]
    results = {}
    
    # Strategy 1: Random
    indices_r = random.sample(range(len(rows)), 50)
    best_r, best_idx_r = float('inf'), -1
    for i in indices_r:
        score = get_score(header, label(i))
        if score < best_r:
            best_r, best_idx_r = score, i
    results["random"] = (best_r, best_idx_r)

    # Strategy 2: Greedy (1 random, then local search)
    curr = random.randint(0, len(rows) - 1)
    for _ in range(49):
        # Look at 5 random neighbors in the dataset
        neighbors = random.sample(range(len(rows)), 5)
        best_n, best_idx_n = float('inf'), -1
        for n in neighbors:
            score = get_score(header, label(n))
            if score < best_n:
                best_n, best_idx_n = score, n
        curr = best_idx_n
    results["greedy"] = (get_score(header, label(curr)), curr)

    # Strategy 3: Explore (25 random, then 25 neighbors of best)
    indices_e = random.sample(range(len(rows)), 25)
    best_e, best_idx_e = float('inf'), -1
    for i in indices_e:
        score = get_score(header, label(i))
        if score < best_e:
            best_e, best_idx_e = score, i
    for _ in range(25):
        n = random.randint(0, len(rows) - 1)
        score = get_score(header, label(n))
        if score < best_e:
            best_e, best_idx_e = score, n
    results["explore"] = (best_e, best_idx_e)

    # Determine winner
    winner = min(results, key=lambda k: results[k][0])
    return {"winner": winner, "row": results[winner][1], "tried": tried}

if __name__ == "__main__":
    filename = "pom3a.train.csv"
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)
        
    # Pre-extract true goals for the label function
    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    true_goals = [[float(row[i]) for i in goal_indices] for row in rows]

    def label(i):
        return true_goals[i]

    outcome = race(header, rows, label)
    
    print("Consultant Race Results:")
    print(f"Winner: {outcome['winner']}")
    print(f"Best Row Found Index: {outcome['row']}")
    print(f"Strategies Compared: {', '.join(outcome['tried'])}")
