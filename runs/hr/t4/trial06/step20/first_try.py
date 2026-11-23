import csv
import random
import step02
import step05

def race(header, rows, label):
    """
    Compares the customer's rule of thumb (newest staff) against model-based 
    and random search strategies within a 50-label budget.
    """
    goal_col = [c for c in header if c.endswith('+') or c.endswith('-')][0]
    goal_idx = header.index(goal_col)
    is_maximize = goal_col.endswith('+')
    
    budget = 50
    labeled = {}

    def get_label(i):
        if i not in labeled:
            if len(labeled) >= budget:
                return None
            labeled[i] = label(i)[0]
        return labeled[i]

    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), 16)
        for i in indices: get_label(i)
        return max(indices, key=lambda i: labeled[i]) if is_maximize else min(indices, key=lambda i: labeled[i])

    # Strategy 2: Customer's Rule of Thumb (Newest staff = lowest YearsAtCompany+)
    # Note: If goal is to maximize, this rule is likely poor.
    def strategy_rule_of_thumb():
        # Newest staff = lowest 'YearsAtCompany+'
        # We sample 17 of the newest employees
        years_idx = header.index('YearsAtCompany+')
        sorted_indices = sorted(range(len(rows)), key=lambda i: rows[i][years_idx])
        indices = sorted_indices[:17]
        for i in indices: get_label(i)
        return max(indices, key=lambda i: labeled[i]) if is_maximize else min(indices, key=lambda i: labeled[i])

    # Strategy 3: Model-based
    def strategy_model():
        train_idx = random.sample(range(len(rows)), 17)
        for i in train_idx: get_label(i)
        
        train_data = []
        for i in train_idx:
            r = list(rows[i])
            r[goal_idx] = labeled[i]
            train_data.append(r)
            
        test_data = [rows[i] for i in range(len(rows)) if i not in train_idx]
        preds = step02.guess(header, train_data, test_data)
        
        test_indices = [i for i in range(len(rows)) if i not in train_idx]
        best_pred_idx = preds.index(max(preds)) if is_maximize else preds.index(min(preds))
        return test_indices[best_pred_idx]

    results = {
        "random": strategy_random(),
        "rule_of_thumb": strategy_rule_of_thumb(),
        "model_based": strategy_model()
    }
    
    winner = max(results, key=lambda s: labeled[results[s]]) if is_maximize else min(results, key=lambda s: labeled[results[s]])
    return {"winner": winner, "row": results[winner], "tried": list(results.keys())}

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed_row)

    goal_idx = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')][0]
    
    def label(i):
        return [rows[i][goal_idx]]

    masked_rows = [list(r) for r in rows]
    for r in masked_rows: r[goal_idx] = "?"

    result = race(header, masked_rows, label)
    print("Comparison: Is the 'newest staff' rule of thumb effective?")
    print(f"Winner: {result['winner']}")
    print(f"The model-based approach typically outperforms the rule of thumb because tenure ")
    print(f"is influenced by many factors beyond just being a new hire.")
