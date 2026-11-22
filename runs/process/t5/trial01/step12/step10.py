import ezr
import random

def race(header, rows, label):
    """
    Compares three strategies: random, acquire, and distance.
    Total budget of 50 labels shared across all.
    """
    budget = 50
    labeled_data = {}

    def get_label(i):
        nonlocal budget
        if i not in labeled_data:
            if budget <= 0:
                return None
            labeled_data[i] = label(i)
            budget -= 1
        return labeled_data[i]

    # Initialize table with header and rows (rows have '?' for goals)
    tbl = ezr.Tbl([header] + rows)

    def strategy_random(tbl, rows):
        indices = random.sample(range(len(rows)), 16)
        for i in indices:
            get_label(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, get_label(i)))

    def strategy_acquire(tbl, rows):
        # Use ezr.acquire logic with a custom oracle
        def oracle_wrapper(row):
            # Find index by matching row object
            idx = next(i for i, r in enumerate(rows) if r is row)
            return get_label(idx)
        
        # Acquire returns rows, we need to map back to indices
        best_rows = ezr.acquire(tbl, cap=17, label=oracle_wrapper)
        # Return index of the best row found by this strategy
        return min([i for i, r in enumerate(rows) if r in best_rows], 
                   key=lambda i: ezr.ydist(tbl, get_label(i)))

    def strategy_distance(tbl, rows):
        # Search for rows closest to the centroid
        centroid = ezr.mids(tbl)
        scored = []
        for i, row in enumerate(rows):
            scored.append((ezr.xdist(tbl, row, centroid), i))
        scored.sort()
        indices = [x[1] for x in scored[:17]]
        for i in indices:
            get_label(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, get_label(i)))

    strategies = {
        "random": strategy_random,
        "acquire": strategy_acquire,
        "distance": strategy_distance
    }

    results = {}
    for name, func in strategies.items():
        best_idx = func(tbl, rows)
        results[name] = (best_idx, ezr.ydist(tbl, get_label(best_idx)))

    winner = min(results, key=lambda n: results[n][1])
    return {
        "winner": winner,
        "row": int(results[winner][0]),
        "tried": list(strategies.keys())
    }

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    rows_iter = ezr.csv(filename)
    header = next(rows_iter)
    all_rows = list(rows_iter)
    
    # Mask goals
    hidden_rows = []
    for row in all_rows:
        new_row = list(row)
        for i, name in enumerate(header):
            if name[-1] in "+-":
                new_row[i] = "?"
        hidden_rows.append(new_row)
        
    def label_func(i):
        return all_rows[i]
    
    random.seed(1234567891)
    result = race(header, hidden_rows, label_func)
    
    print("Race Results:")
    print(f"Winner: {result['winner']}")
    print(f"Best row index found: {result['row']}")
    print(f"Strategies tried: {', '.join(result['tried'])}")
    exit(0)
