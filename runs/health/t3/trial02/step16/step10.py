import csv
import random

def race(header, rows, label):
    """
    Compares three strategies:
    1. 'random': Picks rows at random.
    2. 'first_n': Picks the first 16 rows sequentially.
    3. 'last_n': Picks the last 17 rows sequentially.
    Total budget: 50 labels.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    
    def get_score(row_goals):
        score = 0
        for i, g_idx in enumerate(goal_indices):
            val = row_goals[i]
            # Normalize: MRE- (minimize), ACC+ (maximize), PRED40+ (maximize)
            # We use a simple heuristic: lower is better for -, higher for +
            if header[g_idx].endswith('-'):
                score -= val
            else:
                score += val
        return score

    strategies = {
        "random": random.sample(range(len(rows)), 17),
        "first_n": list(range(16)),
        "last_n": list(range(len(rows) - 17, len(rows)))
    }

    best_overall_score = float('-inf')
    winner = None
    best_row_idx = -1

    for name, indices in strategies.items():
        for idx in indices:
            goals = label(idx)
            score = get_score(goals)
            if score > best_overall_score:
                best_overall_score = score
                best_row_idx = idx
                winner = name

    return {
        "winner": winner,
        "row": best_row_idx,
        "tried": list(strategies.keys())
    }

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    header = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                try:
                    processed_row.append(float(val))
                except ValueError:
                    processed_row.append(val)
            rows.append(processed_row)

    # Store true goals to simulate the label function
    true_goals = {i: [row[j] for j, h in enumerate(header) if h.endswith('-') or h.endswith('+')] 
                  for i, row in enumerate(rows)}
    
    def label(i):
        return true_goals[i]

    result = race(header, rows, label)
    
    print("Race Analysis:")
    print(f"The winning strategy was: {result['winner']}")
    print(f"The best row found was at index: {result['row']}")
    print(f"Strategies compared: {', '.join(result['tried'])}")
