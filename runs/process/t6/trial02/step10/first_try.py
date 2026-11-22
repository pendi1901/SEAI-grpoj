import ezr
import step01
import step07
import random

def race(header, rows, label):
    """
    Compare three strategies: random, greedy (acquire), and a simple 
    distance-based heuristic. Budget is 50 labels total.
    """
    budget = 50
    # Shared cache to ensure we don't exceed the 50-label limit
    labeled_cache = {}

    def oracle_wrapper(idx):
        if idx not in labeled_cache:
            if len(labeled_cache) >= budget:
                raise Exception("Budget exceeded")
            labeled_cache[idx] = label(idx)
        return labeled_cache[idx]

    # 1. Random Strategy
    def strategy_random():
        indices = random.sample(range(len(rows)), budget // 3)
        best = min(indices, key=lambda i: ezr.ydist(tbl, oracle_wrapper(i)))
        return best

    # 2. Acquire Strategy (from step07)
    def strategy_acquire():
        # Use a local copy of rows to avoid modifying the original
        local_rows = [list(r) for r in rows]
        def smart_label(idx):
            full = oracle_wrapper(idx)
            for i in range(len(local_rows[idx])): local_rows[idx][i] = full[i]
            return full
        
        # We use a subset of the budget for this strategy
        best_idx = step07.choose(header, local_rows, smart_label)
        return best_idx

    # 3. Heuristic Strategy (Closest to centroid)
    def strategy_centroid():
        tbl = ezr.Tbl([header] + rows)
        centroid = ezr.mids(tbl)
        # Pick rows closest to the centroid
        candidates = sorted(range(len(rows)), key=lambda i: ezr.xdist(tbl, rows[i], centroid))
        best = min(candidates[:budget // 3], key=lambda i: ezr.ydist(tbl, oracle_wrapper(i)))
        return best

    tbl = ezr.Tbl([header] + rows)
    
    results = {
        "random": strategy_random(),
        "acquire": strategy_acquire(),
        "centroid": strategy_centroid()
    }
    
    # Determine winner: lowest ydist
    winner = min(results, key=lambda name: ezr.ydist(tbl, oracle_wrapper(results[name])))
    
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
