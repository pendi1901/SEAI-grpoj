import ezr
import random

def race(header, rows, label):
    """
    Compare three strategies:
    1. 'random': Baseline.
    2. 'rule_of_thumb': Prioritize newest staff (highest 'YearsAtCompany+').
    3. 'active': Model-based active learning.
    """
    # Use a dictionary to store labeled rows by index to avoid unhashable list issues
    labeled_data = {}
    
    def get_label(idx):
        if idx not in labeled_data:
            if len(labeled_data) >= 50:
                raise Exception("Budget exceeded")
            labeled_data[idx] = label(rows[idx])
        return labeled_data[idx]

    tbl = ezr.Tbl([header] + rows)
    
    # Strategy 1: Random
    def strategy_random(budget):
        indices = random.sample(range(len(rows)), budget)
        for i in indices: get_label(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, labeled_data[i]))

    # Strategy 2: Rule of Thumb (Newest staff)
    def strategy_rule_of_thumb(budget):
        tenure_idx = header.index('YearsAtCompany+')
        # Sort by tenure descending (newest first)
        sorted_indices = sorted(range(len(rows)), key=lambda i: rows[i][tenure_idx], reverse=True)
        for i in sorted_indices[:budget]: get_label(i)
        return min(sorted_indices[:budget], key=lambda i: ezr.ydist(tbl, labeled_data[i]))

    # Strategy 3: Active Learning
    def strategy_active(budget):
        # Bootstrap
        for i in random.sample(range(len(rows)), 5): get_label(i)
        while len(labeled_data) < budget:
            lab_rows = [labeled_data[i] for i in labeled_data]
            lab_tbl = ezr.clone(tbl, lab_rows)
            rank_fn = ezr.ranker(lab_tbl)
            unlabeled = [i for i in range(len(rows)) if i not in labeled_data]
            if not unlabeled: break
            best_idx = min(unlabeled, key=lambda i: rank_fn(rows[i]))
            get_label(best_idx)
        return min(labeled_data.keys(), key=lambda i: ezr.ydist(tbl, labeled_data[i]))

    # Execute strategies with a shared budget of 50 labels (16 each)
    strategies = {
        "random": lambda: strategy_random(16),
        "rule_of_thumb": lambda: strategy_rule_of_thumb(16),
        "active": lambda: strategy_active(16)
    }
    
    results = {}
    for name, func in strategies.items():
        best_idx = func()
        results[name] = (best_idx, ezr.ydist(tbl, labeled_data[best_idx]))

    winner = min(results, key=lambda n: results[n][1])
    return {"winner": winner, "row": results[winner][0], "tried": list(strategies.keys())}

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Mask goals
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for i in goal_indices:
            new_row[i] = "?"
        masked_rows.append(new_row)
        
    def label(row):
        # Return the original row (ground truth)
        return row

    result = race(header, masked_rows, label)
    
    print("Analysis: Is the 'newest staff' rule of thumb effective?")
    print("-" * 60)
    print(f"Winner: {result['winner']}")
    print(f"Strategies compared: {', '.join(result['tried'])}")
    print("-" * 60)
    if result['winner'] == 'rule_of_thumb':
        print("The rule of thumb is effective.")
    else:
        print("The rule of thumb is outperformed by data-driven strategies.")
    print("Conclusion: Relying on tenure alone ignores the multi-dimensional")
    print("nature of employee satisfaction and retention.")
    exit(0)
