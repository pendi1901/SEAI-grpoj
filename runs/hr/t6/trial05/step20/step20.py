import ezr
import random

def race(header, rows, label):
    """
    Compares three strategies:
    1. 'random': Randomly picks rows.
    2. 'tenure_rule': The customer's rule (biggest pay rises to newest staff).
    3. 'acquire': The intelligent search strategy.
    """
    budget = 50
    labeled_cache = {}

    def oracle_wrapper(i):
        if i not in labeled_cache:
            if len(labeled_cache) >= budget:
                raise Exception("Budget exceeded")
            labeled_cache[i] = label(i)
        return labeled_cache[i]

    # Initialize table with a few samples to define goal columns
    # We must ensure we use the full row structure including goals
    initial_indices = list(range(min(len(rows), 5)))
    initial_data = [label(i) for i in initial_indices]
    tbl = ezr.Tbl([header] + initial_data)
    
    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), budget // 3)
        for i in indices: oracle_wrapper(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, oracle_wrapper(i)))

    # Strategy 2: Customer's Rule (Newest staff = lowest YearsAtCompany+)
    def strategy_tenure_rule():
        col_map = {name: i for i, name in enumerate(header)}
        tenure_idx = col_map['YearsAtCompany+']
        # Sort by tenure ascending (newest first)
        indices = sorted(range(len(rows)), key=lambda i: rows[i][tenure_idx])
        subset = indices[:budget // 3]
        for i in subset: oracle_wrapper(i)
        return min(subset, key=lambda i: ezr.ydist(tbl, oracle_wrapper(i)))

    # Strategy 3: Acquire
    def strategy_acquire():
        def label_func(row):
            # Find index of row in original rows list
            for i, r in enumerate(rows):
                if r is row:
                    return oracle_wrapper(i)
            return row
        
        # Use a small subset to seed the acquire process
        seed_indices = random.sample(range(len(rows)), 5)
        labeled_rows = [oracle_wrapper(i) for i in seed_indices]
        lab_tbl = ezr.clone(tbl, labeled_rows)
        
        best_row = min(ezr.acquire(lab_tbl, cap=budget // 3, label=label_func), 
                       key=lambda r: ezr.ydist(tbl, r))
        # Find index of best_row
        for i, r in enumerate(rows):
            if r is best_row:
                return i
        return 0

    results = {
        "random": strategy_random(),
        "tenure_rule": strategy_tenure_rule(),
        "acquire": strategy_acquire()
    }

    winner = min(results, key=lambda name: ezr.ydist(tbl, oracle_wrapper(results[name])))
    
    return {
        "winner": winner,
        "row": results[winner],
        "tried": list(results.keys())
    }

if __name__ == "__main__":
    data = list(ezr.csv("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"))
    header = data[0]
    rows = data[1:]
    
    masked_rows = []
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)

    def label(i):
        return rows[i]

    result = race(header, masked_rows, label)
    
    print("Analysis: Is the 'newest staff' rule of thumb effective?")
    print(f"The winning strategy was: {result['winner']}")
    if result['winner'] == "tenure_rule":
        print("Yes, the rule of thumb is effective.")
    else:
        print("No, the rule of thumb is outperformed by more intelligent search strategies.")
    
    exit(0)
