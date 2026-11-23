import csv
import random

def race(header, rows, label):
    """
    Compares three strategies: 'random', 'greedy', and 'hill_climber'.
    Budget: 50 labels total.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    
    def get_score(goals):
        # Normalize goals: minimize '-' (val), maximize '+' (1-val)
        score = 0
        for i, val in enumerate(goals):
            name = header[goal_indices[i]]
            if name.endswith('-'):
                score += val
            else:
                score += (1 - val)
        return score

    labeled = {}
    def get_label(i):
        if i not in labeled:
            if len(labeled) >= 50:
                raise Exception("Budget exceeded")
            labeled[i] = label(i)
        return labeled[i]

    # Strategies
    def strategy_random():
        best_idx = -1
        best_score = float('inf')
        for _ in range(16): # 16 labels
            idx = random.randint(0, len(rows) - 1)
            score = get_score(get_label(idx))
            if score < best_score:
                best_score, best_idx = score, idx
        return best_idx

    def strategy_greedy():
        # Sample 17, pick best
        best_idx = -1
        best_score = float('inf')
        for _ in range(17):
            idx = random.randint(0, len(rows) - 1)
            score = get_score(get_label(idx))
            if score < best_score:
                best_score, best_idx = score, idx
        return best_idx

    def strategy_hill_climber():
        # Start random, then move to neighbors
        curr = random.randint(0, len(rows) - 1)
        curr_score = get_score(get_label(curr))
        for _ in range(16):
            neighbor = random.randint(0, len(rows) - 1)
            n_score = get_score(get_label(neighbor))
            if n_score < curr_score:
                curr, curr_score = neighbor, n_score
        return curr

    results = {
        "random": strategy_random(),
        "greedy": strategy_greedy(),
        "hill_climber": strategy_hill_climber()
    }

    # Determine winner
    best_overall_score = float('inf')
    winner = None
    best_row = -1
    for name, idx in results.items():
        score = get_score(get_label(idx))
        if score < best_overall_score:
            best_overall_score, winner, best_row = score, name, idx
            
    return {"winner": winner, "row": best_row, "tried": list(results.keys())}

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(x) for x in row])
        
        goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
        
        def label(i):
            return [rows[i][idx] for idx in goal_indices]
            
        result = race(header, rows, label)
        print(f"The winning strategy is: {result['winner']}")
        print(f"Best configuration found at index: {result['row']}")
        print(f"Strategies compared: {', '.join(result['tried'])}")
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
