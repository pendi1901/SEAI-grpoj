import csv
import random

def race(header, rows, label):
    """
    Compares three strategies to find the best row (highest 'YearsAtCompany+')
    using a shared budget of 50 labels.
    
    Strategies:
    1. 'random': Picks 50 rows at random.
    2. 'rule_of_thumb': Targets the newest staff (lowest 'YearsAtCompany+') 
       assuming they need the biggest pay rises to stay.
    3. 'tenure_focus': Targets the most experienced staff (highest 'TotalWorkingYears').
    """
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+'))
    years_idx = header.index('TotalWorkingYears')
    tenure_idx = header.index('YearsAtCompany+')
    
    # Budget: 50 labels total
    # We split the budget: 16 for random, 17 for rule_of_thumb, 17 for tenure_focus
    
    def get_val(idx):
        return label(idx)[0]

    def random_strategy(budget):
        indices = random.sample(range(len(rows)), budget)
        best_idx = -1
        best_val = -float('inf')
        for idx in indices:
            val = get_val(idx)
            if val > best_val:
                best_val = val
                best_idx = idx
        return best_idx

    def rule_of_thumb_strategy(budget):
        # Rule of thumb: give biggest pay rises to newest staff.
        # We test if this actually finds the "best" (highest tenure) employees.
        # Sort by tenure ascending (newest first)
        sorted_indices = sorted(range(len(rows)), key=lambda i: rows[i][tenure_idx])
        best_idx = -1
        best_val = -float('inf')
        for idx in sorted_indices[:budget]:
            val = get_val(idx)
            if val > best_val:
                best_val = val
                best_idx = idx
        return best_idx

    def tenure_focus_strategy(budget):
        # Focus on those with highest total working years
        sorted_indices = sorted(range(len(rows)), key=lambda i: rows[i][years_idx], reverse=True)
        best_idx = -1
        best_val = -float('inf')
        for idx in sorted_indices[:budget]:
            val = get_val(idx)
            if val > best_val:
                best_val = val
                best_idx = idx
        return best_idx

    strategies = {
        "random": (random_strategy, 16),
        "rule_of_thumb": (rule_of_thumb_strategy, 17),
        "tenure_focus": (tenure_focus_strategy, 17)
    }
    
    results = {}
    best_overall_idx = -1
    best_overall_val = -float('inf')
    
    for name, (func, budget) in strategies.items():
        idx = func(budget)
        results[name] = idx
        val = get_val(idx)
        if val > best_overall_val:
            best_overall_val = val
            best_overall_idx = idx
            
    winner = max(results, key=lambda n: get_val(results[n]))
    
    return {
        "winner": winner,
        "row": results[winner],
        "tried": list(strategies.keys())
    }

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
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

    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+'))
    true_goals = [[row[goal_idx]] for row in rows]
    for row in rows:
        row[goal_idx] = "?"

    labeled = set()
    def label(i):
        if len(labeled) >= 50 and i not in labeled:
            raise ValueError("Budget exceeded")
        labeled.add(i)
        return true_goals[i]

    result = race(header, rows, label)
    print("Customer Analysis: Is the 'newest staff' rule of thumb effective?")
    print(f"Winner Strategy: {result['winner']}")
    print(f"The 'rule_of_thumb' strategy was compared against random and tenure-based searches.")
    if result['winner'] == 'rule_of_thumb':
        print("Conclusion: Your rule of thumb is effective for identifying high-tenure employees.")
    else:
        print("Conclusion: Your rule of thumb is outperformed by other search strategies.")
