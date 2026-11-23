import ezr
import random
import step01
import step07

def race(header, rows, label):
    """
    Compares three strategies: random, greedy (acquire), and a simple 
    distance-based search. Total budget is 50 labels.
    """
    budget = 50
    # Shared oracle wrapper to enforce the 50-label limit
    labeled_indices = set()

    def oracle_wrapper(idx):
        if len(labeled_indices) >= budget and idx not in labeled_indices:
            raise Exception("Budget exceeded")
        labeled_indices.add(idx)
        return label(idx)

    # Strategy 1: Random
    def strategy_random(tbl):
        indices = random.sample(range(len(rows)), budget // 3)
        for i in indices:
            true_row = oracle_wrapper(i)
            for j in range(len(true_row)): rows[i][j] = true_row[j]
            ezr.addCols(tbl, rows[i])
        return min(range(len(rows)), key=lambda i: ezr.ydist(tbl, rows[i]))

    # Strategy 2: Acquire (Greedy)
    def strategy_acquire(tbl):
        # We use a local copy of rows to not interfere with other strategies
        # but we must use the shared oracle_wrapper
        def local_oracle(idx):
            true_row = oracle_wrapper(idx)
            rows[idx] = true_row
            return true_row
        
        # Use ezr.acquire logic
        best_idx = step07.choose(header, rows, local_oracle)
        return best_idx

    # Strategy 3: Distance-based (Spot-based)
    def strategy_spot(tbl):
        # Pick rows that are most 'suspicious' (far from centroid)
        # and label them to see if they are actually good
        import step09
        indices = step09.spot(header, rows)[:budget // 3]
        for i in indices:
            true_row = oracle_wrapper(i)
            for j in range(len(true_row)): rows[i][j] = true_row[j]
            ezr.addCols(tbl, rows[i])
        return min(range(len(rows)), key=lambda i: ezr.ydist(tbl, rows[i]))

    # Run the race
    tbl = ezr.Tbl([header] + rows)
    results = {
        "random": strategy_random(ezr.clone(tbl)),
        "acquire": strategy_acquire(ezr.clone(tbl)),
        "spot": strategy_spot(ezr.clone(tbl))
    }

    # Determine winner (lowest ydist)
    best_name = min(results, key=lambda name: ezr.ydist(tbl, rows[results[name]]))
    
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
