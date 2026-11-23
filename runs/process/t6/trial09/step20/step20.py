import ezr
import random
import step07

def race(header, rows, label):
    """
    Compares three strategies: random, greedy (acquire), and 'big-team'.
    Total budget is 50 labels.
    """
    budget = 50
    labeled_indices = {}

    def oracle_wrapper(idx):
        if idx not in labeled_indices:
            if len(labeled_indices) >= budget:
                raise Exception("Budget exceeded")
            labeled_indices[idx] = label(idx)
        return labeled_indices[idx]

    # Strategy 1: Random
    def strategy_random(tbl):
        indices = random.sample(range(len(rows)), budget // 3)
        for i in indices:
            oracle_wrapper(i)
        return min(range(len(rows)), key=lambda i: ezr.ydist(tbl, oracle_wrapper(i)))

    # Strategy 2: Acquire (Greedy)
    def strategy_acquire(tbl):
        # We pass a wrapper that uses our shared labeled_indices
        return step07.choose(header, rows, oracle_wrapper)

    # Strategy 3: Big-Team (Customer's current way: pick rows with high Team Size)
    def strategy_big_team(tbl):
        # Team Size is at index 8
        team_size_idx = 8
        candidates = sorted(range(len(rows)), key=lambda i: rows[i][team_size_idx], reverse=True)
        indices = candidates[:budget // 3]
        for i in indices:
            oracle_wrapper(i)
        return min(range(len(rows)), key=lambda i: ezr.ydist(tbl, oracle_wrapper(i)))

    # Run the race
    results = {}
    # We must re-initialize the table for each strategy to ensure fair evaluation
    for name, func in [("random", strategy_random), 
                       ("acquire", strategy_acquire), 
                       ("big-team", strategy_big_team)]:
        tbl = ezr.Tbl([header])
        # Add all currently labeled rows to the table to establish normalization
        for idx, row in labeled_indices.items():
            ezr.addRow(tbl, row)
        results[name] = func(tbl)

    # Determine winner (lowest ydist)
    final_tbl = ezr.Tbl([header])
    for row in labeled_indices.values():
        ezr.addRow(final_tbl, row)
        
    best_name = min(results, key=lambda name: ezr.ydist(final_tbl, labeled_indices[results[name]]))
    
    return {
        "winner": best_name,
        "row": results[best_name],
        "tried": list(results.keys())
    }

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    full_data = list(ezr.csv(filename))
    header = full_data[0]
    full_rows = full_data[1:]
    
    # Mask goals
    rows = []
    for r in full_rows:
        new_row = r[:]
        for i, h in enumerate(header):
            if h[-1] in "+-": new_row[i] = "?"
        rows.append(new_row)
    
    def label(idx): return full_rows[idx]
    
    outcome = race(header, rows, label)
    
    print("Strategy Comparison Report:")
    print(f"The winning strategy is: {outcome['winner']}")
    print(f"Strategies evaluated: {', '.join(outcome['tried'])}")
    exit(0)
