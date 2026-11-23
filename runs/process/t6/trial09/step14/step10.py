import ezr
import random
import step07
import step09

def race(header, rows, label):
    """
    Compares three strategies: random, greedy (acquire), and spot-based.
    Total budget is 50 labels.
    """
    budget = 50
    labeled_indices = set()

    def oracle_wrapper(idx):
        if len(labeled_indices) >= budget and idx not in labeled_indices:
            raise Exception("Budget exceeded")
        labeled_indices.add(idx)
        return label(idx)

    # Helper to update rows and table
    def update_row(tbl, idx):
        if idx not in labeled_indices:
            true_row = oracle_wrapper(idx)
            rows[idx] = true_row
            ezr.addCols(tbl, true_row)

    # Strategy 1: Random
    def strategy_random(tbl):
        indices = random.sample(range(len(rows)), budget // 3)
        for i in indices:
            update_row(tbl, i)
        return min(range(len(rows)), key=lambda i: ezr.ydist(tbl, rows[i]))

    # Strategy 2: Acquire (Greedy)
    def strategy_acquire(tbl):
        # We use a local oracle wrapper that updates the shared rows
        def local_oracle(idx):
            update_row(tbl, idx)
            return rows[idx]
        return step07.choose(header, rows, local_oracle)

    # Strategy 3: Spot-based
    def strategy_spot(tbl):
        indices = step09.spot(header, rows)[:budget // 3]
        for i in indices:
            update_row(tbl, i)
        return min(range(len(rows)), key=lambda i: ezr.ydist(tbl, rows[i]))

    # Run the race
    # We need a fresh table for each strategy to ensure normalization is consistent
    results = {}
    for name, func in [("random", strategy_random), 
                       ("acquire", strategy_acquire), 
                       ("spot", strategy_spot)]:
        tbl = ezr.Tbl([header] + rows)
        results[name] = func(tbl)

    # Determine winner (lowest ydist)
    # Re-evaluate all strategies on a final table containing all labeled data
    final_tbl = ezr.Tbl([header] + rows)
    best_name = min(results, key=lambda name: ezr.ydist(final_tbl, rows[results[name]]))
    
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
    print(f"Race Results:")
    print(f"Winner: {outcome['winner']}")
    print(f"Best row index found: {outcome['row']}")
    print(f"Strategies tried: {', '.join(outcome['tried'])}")
    exit(0)
