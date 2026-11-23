import csv
import random

def race(header, rows, label):
    """
    Compares three strategies: 'random', 'greedy', and 'exploration'.
    Budget: 50 labels total.
    """
    budget = 50
    tried_indices = set()
    
    goal_indices = [i for i, name in enumerate(header) if '-' in name or '+' in name]
    
    def get_score(goals):
        s = 0
        for i, g_idx in enumerate(goal_indices):
            # We don't have global min/max here, so we use a simple relative score
            # based on the assumption that goals are roughly 0-1 scaled.
            if header[g_idx].endswith('-'):
                s -= goals[i]
            else:
                s += goals[i]
        return s

    def get_label(i):
        if i not in tried_indices:
            if len(tried_indices) >= budget:
                raise Exception("Budget exceeded")
            tried_indices.add(i)
        return label(i)

    # Strategy 1: Random
    def strategy_random():
        best_idx = -1
        best_score = -float('inf')
        for _ in range(16): # 16 labels
            idx = random.randint(0, len(rows) - 1)
            score = get_score(get_label(idx))
            if score > best_score:
                best_score = score
                best_idx = idx
        return best_idx

    # Strategy 2: Greedy (Hill climbing)
    def strategy_greedy():
        curr = random.randint(0, len(rows) - 1)
        best_idx = curr
        best_score = get_score(get_label(curr))
        for _ in range(16): # 17 labels total
            neighbor = random.randint(0, len(rows) - 1)
            score = get_score(get_label(neighbor))
            if score > best_score:
                best_score = score
                best_idx = neighbor
        return best_idx

    # Strategy 3: Exploration (Sample and pick best)
    def strategy_exploration():
        indices = random.sample(range(len(rows)), 17) # 17 labels
        best_idx = -1
        best_score = -float('inf')
        for idx in indices:
            score = get_score(get_label(idx))
            if score > best_score:
                best_score = score
                best_idx = idx
        return best_idx

    results = {
        "random": strategy_random(),
        "greedy": strategy_greedy(),
        "exploration": strategy_exploration()
    }
    
    # Determine winner
    winner = None
    best_overall_score = -float('inf')
    best_row_idx = -1
    
    for name, idx in results.items():
        score = get_score(label(idx))
        if score > best_overall_score:
            best_overall_score = score
            best_row_idx = idx
            winner = name
            
    return {"winner": winner, "row": best_row_idx, "tried": ["random", "greedy", "exploration"]}

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    true_goals = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = []
            goals = []
            for i, val in enumerate(row):
                if '-' in header[i] or '+' in header[i]:
                    goals.append(float(val))
                    processed.append("?")
                elif header[i] == 'criterion':
                    processed.append(val)
                else:
                    processed.append(float(val))
            rows.append(processed)
            true_goals.append(goals)

    def label(i):
        return true_goals[i]

    result = race(header, rows, label)
    print(f"Winner: {result['winner']}")
    print(f"Best row index found: {result['row']}")
    print(f"Strategies tried: {', '.join(result['tried'])}")
