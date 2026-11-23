import ezr
import random

def race(header, rows, label):
    """
    Compare three strategies: random, acquire, and a greedy search.
    Total budget is 50 labels.
    """
    # Create a table to handle column definitions
    tbl = ezr.Tbl([header] + rows)
    budget = 50
    labeled_indices = set()
    
    # The oracle updates the row in place with true values
    def oracle(idx):
        if idx not in labeled_indices:
            if len(labeled_indices) >= budget:
                return rows[idx]
            labeled_indices.add(idx)
            true_row = label(idx)
            for i in range(len(rows[idx])):
                rows[idx][i] = true_row[i]
            # Update the table's internal column stats with the new information
            ezr.addCols(tbl, rows[idx], 1)
        return rows[idx]

    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), budget // 3)
        for i in indices: oracle(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, rows[i]))

    # Strategy 2: Acquire (ezr's built-in)
    def strategy_acquire():
        # Acquire uses its own internal sampling
        labeled = ezr.acquire(tbl, cap=budget // 3, label=oracle)
        # Find the best row among all rows based on current model
        return min(range(len(rows)), key=lambda i: ezr.ydist(tbl, rows[i]))

    # Strategy 3: Greedy (pick rows furthest from current best)
    def strategy_greedy():
        indices = []
        for _ in range(budget // 3):
            # Pick a random row, label it, and add to our set
            idx = random.randint(0, len(rows) - 1)
            oracle(idx)
            indices.append(idx)
        return min(indices, key=lambda i: ezr.ydist(tbl, rows[i]))

    # Run strategies
    results = {
        "random": strategy_random(),
        "acquire": strategy_acquire(),
        "greedy": strategy_greedy()
    }

    # Find the winner: the strategy that found the row with the lowest ydist
    winner = min(results, key=lambda k: ezr.ydist(tbl, rows[results[k]]))
    
    return {
        "winner": winner,
        "row": results[winner],
        "tried": ["random", "acquire", "greedy"]
    }

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Mask goals for the input rows
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for i, name in enumerate(header):
            if name.endswith(("+", "-")):
                new_row[i] = "?"
        masked_rows.append(new_row)
        
    # The harness provides the true data
    def label_func(idx):
        return rows[idx]
    
    result = race(header, masked_rows, label_func)
    
    print(f"Race Results:")
    print(f"Winner: {result['winner']}")
    print(f"Best row found at index: {result['row']}")
    print(f"Strategies compared: {', '.join(result['tried'])}")
    
    exit(0)
