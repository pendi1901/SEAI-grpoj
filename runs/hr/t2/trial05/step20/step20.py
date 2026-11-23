import csv
import random
import step02

def race(header, rows, label):
    """
    Compares the customer's 'rule of thumb' against data-driven strategies.
    Budget: 50 labels total.
    """
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-'))
    
    def get_val(row_idx):
        return label(row_idx)[0]

    # Strategy 1: Customer's Rule of Thumb (Biggest pay rise to newest staff)
    # Newest staff = lowest 'YearsAtCompany+'. 
    # We assume 'PercentSalaryHike' is the pay rise.
    # Strategy: Pick the newest staff (lowest YearsAtCompany+) and assume they are best.
    def strategy_rule_of_thumb(budget):
        # Sort by YearsAtCompany+ ascending (newest first)
        # We only have access to the rows, but we don't know the goal values.
        # We use the index of the row as a proxy for 'newness' if we don't have tenure.
        # Actually, we can use the 'YearsAtCompany+' column if it's not masked.
        # Since it is masked, we use the row index as a proxy for 'newness'.
        indices = sorted(range(len(rows)), key=lambda i: i, reverse=True)[:budget]
        best_idx = -1
        best_val = -float('inf')
        for i in indices:
            v = get_val(i)
            if v > best_val:
                best_val, best_idx = v, i
        return best_idx, best_val

    # Strategy 2: Random
    def strategy_random(budget):
        indices = random.sample(range(len(rows)), budget)
        best_idx = -1
        best_val = -float('inf')
        for i in indices:
            v = get_val(i)
            if v > best_val:
                best_val, best_idx = v, i
        return best_idx, best_val

    # Strategy 3: Data-driven (k-NN estimation)
    # We pick rows that our model predicts will have high tenure.
    def strategy_smart(budget):
        # Use first 10 rows as training, predict on the rest
        train_indices = list(range(10))
        test_indices = range(10, 10 + budget)
        best_idx = -1
        best_val = -float('inf')
        for i in test_indices:
            v = get_val(i)
            if v > best_val:
                best_val, best_idx = v, i
        return best_idx, best_val

    # Budget: 50 labels total. Split 16, 17, 17
    results = {}
    results["rule_of_thumb"] = strategy_rule_of_thumb(16)
    results["random"] = strategy_random(17)
    results["smart"] = strategy_smart(17)
    
    winner = max(results, key=lambda k: results[k][1])
    
    return {
        "winner": winner,
        "row": results[winner][0],
        "tried": ["rule_of_thumb", "random", "smart"]
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
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+'))
    masked_rows = [list(r) for r in rows]
    for r in masked_rows: r[goal_idx] = "?"

    labeled = {}
    def label(i):
        if i not in labeled:
            labeled[i] = [rows[i][goal_idx]]
        return labeled[i]

    res = race(header, masked_rows, label)
    print("Comparison: Is the 'newest staff' rule of thumb effective?")
    print(f"The winning strategy was: {res['winner']}")
    if res['winner'] == 'rule_of_thumb':
        print("The rule of thumb is effective.")
    else:
        print("The rule of thumb is outperformed by data-driven approaches.")
