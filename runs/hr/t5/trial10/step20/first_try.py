import ezr
import random

def race(header, rows, label):
    """
    Compare three strategies: random, rule-of-thumb, and our model-based approach.
    Total budget is 50 labels.
    """
    budget = 50
    labeled = {}  # Cache labels to ensure we don't exceed budget

    def get_label(idx):
        if idx not in labeled:
            if len(labeled) >= budget:
                return rows[idx]
            labeled[idx] = label(idx)
        return labeled[idx]

    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), budget // 3)
        for i in indices: get_label(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, get_label(i)))

    # Strategy 2: Rule of Thumb (Biggest pay rise to newest staff)
    # We define "newest" as lowest YearsAtCompany+ (index 31)
    def strategy_rule_of_thumb():
        # Sort by YearsAtCompany+ ascending
        indices = sorted(range(len(rows)), key=lambda i: rows[i][31])
        # Pick the top 16 (budget/3)
        subset = indices[:budget // 3]
        for i in subset: get_label(i)
        return min(subset, key=lambda i: ezr.ydist(tbl, get_label(i)))

    # Strategy 3: Model-based (Acquire)
    def strategy_model():
        # Use ezr's acquire to intelligently pick rows
        # We pass a wrapper to the label function to track budget
        def oracle(row):
            # Find index of this row object
            for i, r in enumerate(rows):
                if r is row:
                    true_row = get_label(i)
                    for j in range(len(row)): row[j] = true_row[j]
                    return row
            return row
        
        tbl_model = ezr.Tbl([header] + rows)
        labeled_rows = ezr.acquire(tbl_model, cap=budget // 3, label=oracle)
        return min(range(len(rows)), key=lambda i: ezr.ydist(tbl, get_label(i)))

    tbl = ezr.Tbl([header] + rows)
    
    results = {
        "random": strategy_random(),
        "rule_of_thumb": strategy_rule_of_thumb(),
        "model": strategy_model()
    }

    # Find the winner: the strategy that found the row with the lowest ydist
    winner = min(results, key=lambda k: ezr.ydist(tbl, get_label(results[k])))
    
    return {
        "winner": winner,
        "row": results[winner],
        "tried": ["random", "rule_of_thumb", "model"]
    }

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Mask goals
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for i, name in enumerate(header):
            if name.endswith(("+", "-")):
                new_row[i] = "?"
        masked_rows.append(new_row)
        
    def label_func(idx):
        return rows[idx]
    
    result = race(header, masked_rows, label_func)
    
    print("Strategy Comparison: Is the 'rule of thumb' effective?")
    print(f"Winner: {result['winner']}")
    print(f"The best strategy was '{result['winner']}'.")
    if result['winner'] == "model":
        print("Our model-based approach outperformed the rule of thumb.")
    elif result['winner'] == "rule_of_thumb":
        print("The rule of thumb is surprisingly effective.")
    else:
        print("Random selection performed best, suggesting the data is highly variable.")
    
    exit(0)
