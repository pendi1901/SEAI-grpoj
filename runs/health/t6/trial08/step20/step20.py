import ezr
import random

def race(header, rows, label):
    """
    Compare three strategies: random, acquire, and a heuristic (top 5% search).
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

    # Initialize the table with the full header to ensure column roles are correct
    # We use a dummy row (or just the header) to initialize the Tbl structure
    tbl = ezr.Tbl([header])

    # Strategy 1: Random
    def strategy_random():
        indices = [random.randint(0, len(rows) - 1) for _ in range(15)]
        for i in indices: get_label(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, get_label(i)))

    # Strategy 2: Acquire
    def strategy_acquire():
        # Use the acquire logic from ezr
        # We need a table that knows about the data distribution
        sub_tbl = ezr.Tbl([header] + random.sample(rows, min(len(rows), 100)))
        
        def oracle_wrapper(row):
            # Find index by matching row
            for i, r in enumerate(rows):
                if r == row: return get_label(i)
            return row
        
        labeled = ezr.acquire(sub_tbl, cap=15, label=oracle_wrapper)
        return min(range(len(rows)), key=lambda i: ezr.ydist(tbl, get_label(i)))

    # Strategy 3: Heuristic (Top 5% search)
    def strategy_heuristic():
        indices = random.sample(range(len(rows)), 15)
        for i in indices: get_label(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, get_label(i)))

    results = {
        "random": strategy_random(),
        "acquire": strategy_acquire(),
        "heuristic": strategy_heuristic()
    }
    
    # Evaluate the best row found by each strategy
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
