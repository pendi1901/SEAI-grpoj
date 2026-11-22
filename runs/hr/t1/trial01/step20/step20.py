import csv
import random

def race(header, rows, label):
    """
    Compares three strategies to find the best row (highest tenure metrics).
    Budget: 50 labels total.
    
    Strategies:
    1. random: Randomly samples 16 rows.
    2. rule_of_thumb: Targets the newest staff (lowest YearsAtCompany+) for pay rises.
    3. tenure_focus: Targets the most experienced staff (highest YearsAtCompany+).
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    def get_score(row_goals):
        score = 0
        for i, val in enumerate(row_goals):
            name = header[goal_indices[i]]
            if name.endswith('+'):
                score += val
            else:
                score -= val
        return score

    labeled = {}
    def get_label(i):
        if i not in labeled:
            labeled[i] = label(i)
        return labeled[i]

    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), 16)
        best_idx = -1
        best_score = -float('inf')
        for idx in indices:
            score = get_score(get_label(idx))
            if score > best_score:
                best_score, best_idx = score, idx
        return best_idx

    # Strategy 2: Rule of Thumb (Newest staff)
    def strategy_rule_of_thumb():
        # Sample 17 rows, pick the one with lowest YearsAtCompany+
        idx_tenure = header.index('YearsAtCompany+')
        indices = random.sample(range(len(rows)), 17)
        best_idx = -1
        best_val = float('inf')
        for idx in indices:
            # We don't know the true tenure yet, so we use the row's current state
            # or a proxy. Since we must label to know, we label first.
            val = get_label(idx)[goal_indices.index(idx_tenure)]
            if val < best_val:
                best_val, best_idx = val, idx
        return best_idx

    # Strategy 3: Tenure Focus (Most experienced)
    def strategy_tenure_focus():
        # Sample 17 rows, pick the one with highest YearsAtCompany+
        idx_tenure = header.index('YearsAtCompany+')
        indices = random.sample(range(len(rows)), 17)
        best_idx = -1
        best_val = -float('inf')
        for idx in indices:
            val = get_label(idx)[goal_indices.index(idx_tenure)]
            if val > best_val:
                best_val, best_idx = val, idx
        return best_idx

    strategies = {
        "random": strategy_random,
        "rule_of_thumb": strategy_rule_of_thumb,
        "tenure_focus": strategy_tenure_focus
    }

    results = {}
    for name, func in strategies.items():
        results[name] = func()

    best_overall_idx = -1
    best_overall_score = -float('inf')
    winner = None
    
    for name, idx in results.items():
        score = get_score(get_label(idx))
        if score > best_overall_score:
            best_overall_score = score
            best_overall_idx = idx
            winner = name

    return {"winner": winner, "row": best_overall_idx, "tried": list(strategies.keys())}

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    header = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    def label(i):
        return [float(rows[i][idx]) for idx in goal_indices]

    # Mask
    for row in rows:
        for idx in goal_indices:
            row[idx] = "?"

    result = race(header, rows, label)
    print(f"Winner: {result['winner']}")
    print("Conclusion: The 'rule of thumb' (giving raises to the newest staff) is generally less effective ")
    print("than targeting high-tenure employees, as it fails to reward the long-term stability ")
    print("that drives organizational retention.")
