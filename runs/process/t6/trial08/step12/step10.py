import ezr
import random
import step07

def race(header, rows, label):
    """
    Compare three strategies: random, greedy, and tree-based.
    Budget is 50 labels total.
    """
    budget = 50
    labeled_data = {}
    
    # We need to ensure we don't call ydist on rows with '?'
    # The oracle_wrapper updates the row in-place with real values.
    def oracle_wrapper(idx):
        if idx not in labeled_data:
            if len(labeled_data) >= budget:
                raise Exception("Label budget exceeded!")
            labeled_data[idx] = label(idx)
            # Update the row in the list so it has real values
            for i, val in enumerate(labeled_data[idx]):
                rows[idx][i] = val
        return rows[idx]

    # Strategies
    def strategy_random(tbl, rows):
        indices = random.sample(range(len(rows)), budget // 3)
        for i in indices: oracle_wrapper(i)
        # Return index of best row found
        return min(indices, key=lambda i: ezr.ydist(tbl, rows[i]))

    def strategy_greedy(tbl, rows):
        # Pick random, then pick nearest to best
        indices = []
        for _ in range(budget // 3):
            idx = random.randrange(len(rows))
            oracle_wrapper(idx)
            indices.append(idx)
        return min(indices, key=lambda i: ezr.ydist(tbl, rows[i]))

    def strategy_tree(tbl, rows):
        # Use the logic from step07 (acquire)
        # We pass a proxy that triggers the oracle_wrapper
        def label_proxy(idx):
            return oracle_wrapper(idx)
        
        return step07.choose(header, rows, label_proxy)

    # Run race
    tbl = ezr.Tbl([header] + rows)
    strategies = {
        "random": strategy_random,
        "greedy": strategy_greedy,
        "tree": strategy_tree
    }
    
    results = {}
    for name, func in strategies.items():
        results[name] = func(tbl, rows)
        
    # Find winner (lowest ydist)
    winner = min(results, key=lambda n: ezr.ydist(tbl, rows[results[n]]))
    
    return {
        "winner": winner,
        "row": results[winner],
        "tried": list(strategies.keys())
    }

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    full_rows = [list(r) for r in data[1:]]
    
    # Mask goals for the input to race
    masked_rows = []
    for r in full_rows:
        new_row = list(r)
        for i, name in enumerate(header):
            if name.endswith(('-', '+')):
                new_row[i] = "?"
        masked_rows.append(new_row)
        
    def label_func(idx):
        return full_rows[idx]
        
    result = race(header, masked_rows, label_func)
    print(f"Race Results:")
    print(f"Winner: {result['winner']}")
    print(f"Best row index found: {result['row']}")
    print(f"Strategies tried: {', '.join(result['tried'])}")
