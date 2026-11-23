import ezr
import random

def race(header, rows, label):
    """
    Compares the customer's rule of thumb against data-driven strategies.
    Budget: 50 labels total.
    """
    labeled = {}

    def get_label(i):
        if i not in labeled:
            if len(labeled) >= 50:
                raise Exception("Budget exceeded")
            labeled[i] = label(i)
        return labeled[i]

    # We need a table that has seen all labeled data to calculate ydist correctly
    # We will update this table as we label rows.
    tbl = ezr.Tbl([header])

    def update_tbl(row):
        ezr.addRow(tbl, row)

    # Strategy 1: Customer's rule of thumb (Newest staff = lowest YearsAtCompany)
    def strategy_rule_of_thumb(budget):
        idx_tenure = header.index("YearsAtCompany+")
        sorted_indices = sorted(range(len(rows)), key=lambda i: rows[i][idx_tenure])
        indices = sorted_indices[:budget]
        for i in indices:
            update_tbl(get_label(i))
        return min(indices, key=lambda i: ezr.ydist(tbl, get_label(i)))

    # Strategy 2: Random search
    def strategy_random(budget):
        indices = random.sample(range(len(rows)), budget)
        for i in indices:
            update_tbl(get_label(i))
        return min(indices, key=lambda i: ezr.ydist(tbl, get_label(i)))

    # Strategy 3: Data-driven (Acquire)
    def strategy_data_driven(budget):
        # Use a subset to build the model
        indices = random.sample(range(len(rows)), min(len(rows), 200))
        # Label initial set
        for i in indices[:ezr.the.Start]:
            update_tbl(get_label(i))
        
        # Use acquire to pick the rest
        lab_tbl = ezr.clone(tbl)
        best_rows = ezr.acquire(lab_tbl, cap=budget, label=lambda r: get_label(next(j for j, row in enumerate(rows) if row[9] == r[9])))
        
        # Find the best row index from the labeled set
        best_row = min(best_rows, key=lambda x: ezr.ydist(tbl, x))
        return next(i for i, r in enumerate(rows) if r[9] == best_row[9])

    # Run strategies with a shared budget of 50 (approx 16 each)
    res_rule = strategy_rule_of_thumb(16)
    res_random = strategy_random(17)
    res_data = strategy_data_driven(17)
    
    results = {
        "rule_of_thumb": res_rule,
        "random": res_random,
        "data_driven": res_data
    }
    
    # Determine winner based on lowest ydist
    winner = min(results, key=lambda name: ezr.ydist(tbl, get_label(results[name])))
    
    return {
        "winner": winner,
        "row": results[winner],
        "tried": ["rule_of_thumb", "random", "data_driven"]
    }

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    goal_indices = [i for i, h in enumerate(header) if h.endswith(("+", "-"))]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices: new_row[idx] = "?"
        masked_rows.append(new_row)
        
    def label_func(i):
        return rows[i]
    
    result = race(header, masked_rows, label_func)
    
    print("Analysis: Is the 'newest staff' rule of thumb effective?")
    print(f"Winner of the search strategy race: {result['winner']}")
    
    if result['winner'] == "rule_of_thumb":
        print("Result: Your rule of thumb is highly effective for this dataset.")
    else:
        print("Result: Data-driven approaches outperformed the rule of thumb.")
    
    print(f"Strategies tried: {', '.join(result['tried'])}")
