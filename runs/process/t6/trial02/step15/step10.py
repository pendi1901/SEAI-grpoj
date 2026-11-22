import ezr
import random

def race(header, rows, label):
    """
    Compare three strategies: random, acquire (tree-based), and centroid-based.
    Budget is 50 labels total.
    """
    budget = 50
    labeled_cache = {}

    def oracle_wrapper(idx):
        if idx not in labeled_cache:
            if len(labeled_cache) >= budget:
                raise Exception("Budget exceeded")
            labeled_cache[idx] = label(idx)
        return labeled_cache[idx]

    # Create a base table for distance calculations
    # We use a copy of rows to ensure we don't mutate the original input
    tbl = ezr.Tbl([header] + [list(r) for r in rows])

    def get_ydist(idx):
        full_row = oracle_wrapper(idx)
        return ezr.ydist(tbl, full_row)

    # 1. Random Strategy
    def strategy_random():
        indices = random.sample(range(len(rows)), budget // 3)
        return min(indices, key=get_ydist)

    # 2. Acquire Strategy (using ezr's built-in acquire)
    def strategy_acquire():
        # Create a local table for the acquire function
        local_tbl = ezr.Tbl([header] + [list(r) for r in rows])
        
        def smart_label(row):
            # Find index of this row in the original list
            idx = rows.index(row)
            full = oracle_wrapper(idx)
            # Update the row in the local table
            for i in range(len(row)): row[i] = full[i]
            return row
            
        # acquire returns a list of rows, we find the best one
        labeled = ezr.acquire(local_tbl, cap=budget // 3, label=smart_label)
        best_row = min(labeled, key=lambda r: ezr.ydist(local_tbl, r))
        return rows.index(best_row)

    # 3. Centroid Strategy
    def strategy_centroid():
        centroid = ezr.mids(tbl)
        # Pick rows closest to the centroid
        candidates = sorted(range(len(rows)), key=lambda i: ezr.xdist(tbl, rows[i], centroid))
        return min(candidates[:budget // 3], key=get_ydist)

    results = {
        "random": strategy_random(),
        "acquire": strategy_acquire(),
        "centroid": strategy_centroid()
    }
    
    # Determine winner: lowest ydist
    winner = min(results, key=lambda name: get_ydist(results[name]))
    
    return {
        "winner": winner,
        "row": results[winner],
        "tried": list(results.keys())
    }

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    header = next(data_gen)
    all_rows = list(data_gen)
    
    # Mask goals
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    masked_rows = []
    for row in all_rows:
        new_row = list(row)
        for idx in goal_indices: new_row[idx] = "?"
        masked_rows.append(new_row)
        
    def label_func(idx):
        return all_rows[idx]
        
    result = race(header, masked_rows, label_func)
    
    print(f"Race Results:")
    print(f"Winner: {result['winner']}")
    print(f"Best row found at index: {result['row']}")
    print(f"Strategies tried: {', '.join(result['tried'])}")
    
    exit(0)
