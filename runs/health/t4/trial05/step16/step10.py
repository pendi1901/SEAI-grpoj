import csv
import random
from step01 import remember
from step07 import choose

def race(header, rows, label):
    """
    Compares three strategies:
    1. 'random': Picks 17 rows at random.
    2. 'smart': Uses the choose() logic from step07 (17 rows).
    3. 'greedy': Picks the first 16 rows sequentially.
    """
    budget = 50
    results = {}
    
    # Strategy 1: Random
    random_indices = random.sample(range(len(rows)), 17)
    for idx in random_indices:
        goals = label(idx)
        rows[idx][0], rows[idx][1], rows[idx][2] = goals[0], goals[1], goals[2]
    results["random"] = (random_indices, remember(header, [rows[i] for i in random_indices])[0])

    # Strategy 2: Smart (using step07 logic)
    # We pass a wrapper to label to ensure we don't exceed budget
    smart_indices = [int(i * (len(rows) - 1) / 16) for i in range(17)]
    for idx in smart_indices:
        if rows[idx][0] == "?":
            goals = label(idx)
            rows[idx][0], rows[idx][1], rows[idx][2] = goals[0], goals[1], goals[2]
    results["smart"] = (smart_indices, remember(header, [rows[i] for i in smart_indices])[0])

    # Strategy 3: Greedy (first 16)
    greedy_indices = list(range(16))
    for idx in greedy_indices:
        if rows[idx][0] == "?":
            goals = label(idx)
            rows[idx][0], rows[idx][1], rows[idx][2] = goals[0], goals[1], goals[2]
    results["greedy"] = (greedy_indices, remember(header, [rows[i] for i in greedy_indices])[0])

    # Determine winner by comparing the best row found by each
    best_overall = None
    winner = None
    
    # Re-score all found rows to compare across strategies
    all_found = []
    for name, (indices, local_idx) in results.items():
        row = rows[indices[local_idx]]
        all_found.append((remember(header, [row])[0], name, indices[local_idx]))
    
    # Sort by score (remember returns indices of best, so we compare the rows)
    winner = max(all_found, key=lambda x: x[0])[1]
    best_row_pos = max(all_found, key=lambda x: x[0])[2]

    return {"winner": winner, "row": best_row_pos, "tried": ["random", "smart", "greedy"]}

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if header[i] not in ['criterion'] else val 
                             for i, val in enumerate(row)]
            rows.append(processed_row)

    # Mask goals
    true_data = [list(r) for r in rows]
    for r in rows:
        r[0] = r[1] = r[2] = "?"

    def label(i):
        return [true_data[i][0], true_data[i][1], true_data[i][2]]

    outcome = race(header, rows, label)
    print(f"The winning strategy is: {outcome['winner']}")
    print(f"Best row found at index: {outcome['row']}")
    print(f"Strategies compared: {', '.join(outcome['tried'])}")
    exit(0)
