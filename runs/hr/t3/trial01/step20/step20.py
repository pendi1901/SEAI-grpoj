import csv
import random

def race(header, rows, label):
    """
    Compares three strategies to find the best row (highest YearsAtCompany+).
    Budget: 50 labels total.
    
    Strategies:
    1. random: Randomly samples 16 rows.
    2. rule_of_thumb: Targets newest staff (lowest TotalWorkingYears).
    3. high_tenure_potential: Targets staff with high MonthlyIncome (proxy for value).
    """
    goal_idx = next(i for i, h in enumerate(header) if h.endswith('+'))
    
    labeled_cache = {}
    def get_label(i):
        if i not in labeled_cache:
            if len(labeled_cache) >= 50:
                raise Exception("Label budget exceeded")
            labeled_cache[i] = label(i)
        return labeled_cache[i]

    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), 16)
        best_i, best_val = -1, -float('inf')
        for i in indices:
            val = get_label(i)[0]
            if val > best_val:
                best_val, best_i = val, i
        return best_i, best_val

    # Strategy 2: Rule of Thumb (Newest staff = lowest TotalWorkingYears)
    def strategy_rule_of_thumb():
        tenure_idx = header.index('TotalWorkingYears')
        # Pick 17 rows with lowest working years
        indices = sorted(range(len(rows)), key=lambda i: rows[i][tenure_idx])[:17]
        best_i, best_val = -1, -float('inf')
        for i in indices:
            val = get_label(i)[0]
            if val > best_val:
                best_val, best_i = val, i
        return best_i, best_val

    # Strategy 3: High Monthly Income (Heuristic for high-value staff)
    def strategy_high_income():
        income_idx = header.index('MonthlyIncome')
        indices = sorted(range(len(rows)), key=lambda i: rows[i][income_idx], reverse=True)[:17]
        best_i, best_val = -1, -float('inf')
        for i in indices:
            val = get_label(i)[0]
            if val > best_val:
                best_val, best_i = val, i
        return best_i, best_val

    strategies = {
        "random": strategy_random,
        "rule_of_thumb": strategy_rule_of_thumb,
        "high_income": strategy_high_income
    }

    results = {}
    best_overall_val = -float('inf')
    winner = ""
    best_row_idx = -1

    for name, func in strategies.items():
        idx, val = func()
        results[name] = val
        if val > best_overall_val:
            best_overall_val = val
            winner = name
            best_row_idx = idx

    return {"winner": winner, "row": best_row_idx, "tried": list(strategies.keys())}

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed)

    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    true_goals = [[row[i] for i in goal_indices] for row in rows]
    
    # Mask
    for row in rows:
        for i in goal_indices:
            row[i] = "?"

    def label(i):
        return true_goals[i]

    result = race(header, rows, label)
    
    print("Analysis: Is the 'newest staff' rule of thumb effective?")
    print(f"The winning strategy was: {result['winner']}")
    if result['winner'] == 'rule_of_thumb':
        print("Conclusion: Yes, your rule of thumb is effective for finding high-tenure potential.")
    else:
        print("Conclusion: No, other strategies (like targeting high-income staff) outperformed the rule of thumb.")
    print(f"Best row index found: {result['row']}")
