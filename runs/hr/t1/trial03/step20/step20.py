import csv
import random

def get_goal_indices(header):
    return [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]

def get_score(header, row_goals, goal_indices, min_vals, max_vals):
    """Calculates a normalized score [0, 1] for a row based on goal columns."""
    scores = []
    for i, idx in enumerate(goal_indices):
        rng = max_vals[idx] - min_vals[idx]
        rng = rng if rng != 0 else 1
        norm = (row_goals[i] - min_vals[idx]) / rng
        if header[idx].endswith('-'):
            norm = 1 - norm
        scores.append(norm)
    return sum(scores) / len(scores)

def race(header, rows, label):
    """
    Compares three strategies for finding the best employee arrangement.
    1. Random: Baseline.
    2. Rule of Thumb: Biggest pay rises to newest staff (YearsAtCompany+ is low).
    3. Tenure-Based: Biggest pay rises to longest-serving staff (YearsAtCompany+ is high).
    Budget: 50 labels total.
    """
    goal_indices = get_goal_indices(header)
    strategies = ["random", "rule_of_thumb", "tenure_priority"]
    
    # Budget: 16, 17, 17
    budgets = [16, 17, 17]
    results = {}
    
    # 1. Random
    indices_rand = random.sample(range(len(rows)), budgets[0])
    
    # 2. Rule of Thumb: Newest staff (YearsAtCompany+ is low)
    yac_idx = header.index('YearsAtCompany+')
    indices_rot = sorted(range(len(rows)), key=lambda i: rows[i][yac_idx])[:budgets[1]]
    
    # 3. Tenure Priority: Longest-serving staff (YearsAtCompany+ is high)
    indices_ten = sorted(range(len(rows)), key=lambda i: rows[i][yac_idx], reverse=True)[:budgets[2]]
    
    all_indices = indices_rand + indices_rot + indices_ten
    all_goals = {i: label(i) for i in all_indices}
    
    # Global min/max for normalization
    min_vals = {idx: min(all_goals[i][j] for i in all_indices) for j, idx in enumerate(goal_indices)}
    max_vals = {idx: max(all_goals[i][j] for i in all_indices) for j, idx in enumerate(goal_indices)}
    
    # Evaluate strategies
    for name, indices in [("random", indices_rand), ("rule_of_thumb", indices_rot), ("tenure_priority", indices_ten)]:
        best_idx, best_score = -1, -1.0
        for i in indices:
            score = get_score(header, all_goals[i], goal_indices, min_vals, max_vals)
            if score > best_score:
                best_score, best_idx = score, i
        results[name] = (best_idx, best_score)
    
    winner = max(results, key=lambda k: results[k][1])
    return {"winner": winner, "row": results[winner][0], "tried": strategies}

def load_data(filename):
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
    return header, rows

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    header, rows = load_data(filename)
    goal_indices = get_goal_indices(header)
    
    def label(i):
        return [rows[i][idx] for idx in goal_indices]
    
    outcome = race(header, rows, label)
    
    print(f"Winner: {outcome['winner']}")
    print(f"Best row found: {outcome['row']}")
    print(f"Strategies compared: {', '.join(outcome['tried'])}")
    
    if outcome['winner'] == "rule_of_thumb":
        print("\nConclusion: Your rule of thumb is effective.")
    else:
        print("\nConclusion: Your rule of thumb is outperformed by other strategies.")
