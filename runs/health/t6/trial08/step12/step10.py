import ezr
import random

def race(header, rows, label):
    """
    Compare three strategies: random, acquire, and a simple heuristic.
    Budget: 50 labels total.
    """
    budget = 50
    labeled_indices = {}

    def get_label(idx):
        if idx not in labeled_indices:
            if len(labeled_indices) >= budget:
                raise Exception("Budget exceeded")
            labeled_indices[idx] = label(idx)
        return labeled_indices[idx]

    tbl = ezr.Tbl([header] + rows)

    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), 16)
        for i in indices: get_label(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, get_label(i)))

    # Strategy 2: Acquire (using ezr.acquire logic directly)
    def strategy_acquire():
        # We need a table where rows have goals. 
        # Since we can only label 17, we use a subset.
        def oracle_wrapper(row):
            # Find index by matching row (assuming unique rows for this dataset)
            for i, r in enumerate(rows):
                if r == row: return get_label(i)
            return row
        
        # Use a small subset to build the table for acquire
        subset = random.sample(rows, 100)
        sub_tbl = ezr.Tbl([header] + subset)
        labeled = ezr.acquire(sub_tbl, cap=17, label=oracle_wrapper)
        return min(range(len(rows)), key=lambda i: ezr.ydist(tbl, get_label(i)))

    # Strategy 3: Heuristic (Top 5% search)
    def strategy_heuristic():
        indices = random.sample(range(len(rows)), 17)
        for i in indices: get_label(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, get_label(i)))

    results = {
        "random": strategy_random(),
        "acquire": strategy_acquire(),
        "heuristic": strategy_heuristic()
    }
    
    winner = min(results, key=lambda name: ezr.ydist(tbl, get_label(results[name])))
    
    return {
        "winner": winner,
        "row": results[winner],
        "tried": list(results.keys())
    }

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header = next(data_iter)
    rows = list(data_iter)
    
    def label(idx):
        return rows[idx]
    
    result = race(header, rows, label)
    
    print(f"Race complete. Winner: {result['winner']}")
    print(f"Best row found at index: {result['row']}")
    print(f"Strategies compared: {', '.join(result['tried'])}")
    
    exit(0)
