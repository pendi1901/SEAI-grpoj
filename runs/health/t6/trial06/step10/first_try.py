import ezr
import random
import step01
import step07

def race(header, rows, label):
    """
    Compare three strategies for finding the best configuration:
    1. random: Randomly samples rows.
    2. acquire: Uses the active learning strategy from ezr.
    3. greedy: Picks rows based on the best known ydist from a small initial sample.
    """
    budget = 50
    # Track which rows have been labeled to enforce the 50-label limit
    labeled_cache = {}

    def oracle_wrapper(idx):
        if idx not in labeled_cache:
            if len(labeled_cache) >= budget:
                raise Exception("Budget exceeded")
            labeled_cache[idx] = label(idx)
        return labeled_cache[idx]

    # Setup table for distance calculations
    tbl = ezr.Tbl([header] + rows)

    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), budget // 3)
        for i in indices: oracle_wrapper(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, rows[i]))

    # Strategy 2: Acquire (from ezr)
    def strategy_acquire():
        # We pass a wrapper that maps row objects to the oracle
        def label_proxy(row):
            idx = rows.index(row)
            return oracle_wrapper(idx)
        
        # Use the acquire function
        results = ezr.acquire(tbl, cap=budget // 3, label=label_proxy)
        best_row = min(results, key=lambda r: ezr.ydist(tbl, r))
        return rows.index(best_row)

    # Strategy 3: Greedy (Initial sample + pick best)
    def strategy_greedy():
        sample_size = budget // 3
        indices = random.sample(range(len(rows)), sample_size)
        for i in indices: oracle_wrapper(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, rows[i]))

    # Run strategies
    results = {
        "random": strategy_random(),
        "acquire": strategy_acquire(),
        "greedy": strategy_greedy()
    }

    # Determine winner (lowest ydist is best)
    winner = min(results, key=lambda name: ezr.ydist(tbl, rows[results[name]]))
    
    return {
        "winner": winner,
        "row": results[winner],
        "tried": list(results.keys())
    }

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_gen = ezr.csv(filename)
    header = next(data_gen)
    all_rows = list(data_gen)
    
    # Mask goals
    masked_rows = []
    for r in all_rows:
        new_row = list(r)
        for i, name in enumerate(header):
            if name[-1] in "+-":
                new_row[i] = "?"
        masked_rows.append(new_row)
        
    def label(i):
        return all_rows[i]
        
    result = race(header, masked_rows, label)
    print(f"Race Results: {result}")
    print(f"The winning strategy is '{result['winner']}' which found the best row at index {result['row']}.")
