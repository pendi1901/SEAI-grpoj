import csv
import random

def race(header, rows, label):
    """
    Compares three strategies:
    1. 'random': Picks rows at random.
    2. 'big_teams': Picks rows with the largest 'Team Size'.
    3. 'hillclimbing': Starts at a random row and moves to better neighbors.
    
    Total budget: 50 labels shared across all strategies.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    team_size_idx = header.index('Team Size')
    
    def get_score(row_goals):
        score = 0.0
        for i, val in enumerate(row_goals):
            name = header[goal_indices[i]]
            if name.endswith('-'):
                score += val
            else:
                score += (1.0 - val)
        return score

    labeled = {}
    def get_labeled_score(i):
        if i not in labeled:
            if len(labeled) >= 50:
                raise Exception("Budget exceeded")
            labeled[i] = get_score(label(i))
        return labeled[i]

    # Budget: 50 labels total. 
    # We allocate 16 to random, 16 to big_teams, and 18 to hillclimbing.
    results = {}

    # 1. Random Strategy (16 labels)
    best_random_idx = -1
    best_random_score = float('inf')
    for _ in range(16):
        idx = random.randrange(len(rows))
        score = get_labeled_score(idx)
        if score < best_random_score:
            best_random_score = score
            best_random_idx = idx
    results["random"] = (best_random_score, best_random_idx)

    # 2. Big Teams Strategy (16 labels)
    sorted_by_size = sorted(range(len(rows)), key=lambda i: rows[i][team_size_idx], reverse=True)
    best_big_idx = -1
    best_big_score = float('inf')
    for i in sorted_by_size[:16]:
        score = get_labeled_score(i)
        if score < best_big_score:
            best_big_score = score
            best_big_idx = i
    results["big_teams"] = (best_big_score, best_big_idx)

    # 3. Hillclimbing Strategy (Remaining budget: 18 labels)
    curr = random.randrange(len(rows))
    # Initial label counts as 1
    get_labeled_score(curr)
    for _ in range(17):
        neighbors = random.sample(range(len(rows)), 3)
        best_n = min(neighbors, key=get_labeled_score)
        if get_labeled_score(best_n) < get_labeled_score(curr):
            curr = best_n
    results["hillclimbing"] = (get_labeled_score(curr), curr)

    winner = min(results, key=lambda k: results[k][0])
    
    return {
        "winner": winner,
        "row": results[winner][1],
        "tried": ["random", "big_teams", "hillclimbing"]
    }

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(x) for x in row])
        
        def label(i):
            goal_indices = [idx for idx, name in enumerate(header) 
                            if name.endswith('-') or name.endswith('+')]
            return [rows[i][idx] for idx in goal_indices]
        
        outcome = race(header, rows, label)
        
        print("Customer Inquiry: Is 'Big Teams' the best strategy?")
        print("-" * 50)
        print(f"Winner: {outcome['winner']}")
        print(f"Best row found at index: {outcome['row']}")
        print(f"Strategies compared: {', '.join(outcome['tried'])}")
        print("\nAnalysis: We compared your 'big_teams' strategy against")
        print("random sampling and hillclimbing. If 'big_teams' is not")
        print("the winner, it suggests that simply maximizing team size")
        print("is not the most efficient way to optimize your goals.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
