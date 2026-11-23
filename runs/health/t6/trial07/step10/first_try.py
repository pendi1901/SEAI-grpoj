import ezr
import random

def race(header, rows, label):
    """
    Compare three strategies for finding the best row within a 50-label budget.
    Strategies:
    1. random: Randomly samples rows.
    2. acquire: Uses the intelligent acquisition function from ezr.
    3. greedy: Picks the row that looks best based on current knowledge.
    """
    budget = 50
    labeled = {}
    
    def get_label(i):
        if i not in labeled:
            if len(labeled) >= budget:
                raise Exception("Budget exceeded")
            labeled[i] = label(i)
        return labeled[i]

    tbl = ezr.Tbl([header] + rows)
    
    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), budget // 3)
        for i in indices: get_label(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, get_label(i)))

    # Strategy 2: Acquire (from ezr)
    def strategy_acquire():
        # We need to pass a wrapper to acquire that uses our shared label budget
        def oracle_wrapper(row):
            # Find index by matching row (assuming unique rows or index-based)
            # Since we need the index for the label function:
            idx = rows.index(row)
            return get_label(idx)
        
        # We use a subset of the budget
        results = ezr.acquire(tbl, cap=budget // 3, label=oracle_wrapper)
        best_row = min(results, key=lambda r: ezr.ydist(tbl, r))
        return rows.index(best_row)

    # Strategy 3: Greedy (Simple hill climbing)
    def strategy_greedy():
        curr = random.choice(range(len(rows)))
        for _ in range(budget // 3):
            best_n = curr
            best_d = ezr.ydist(tbl, get_label(curr))
            for _ in range(5): # check 5 neighbors
                n = random.randint(0, len(rows) - 1)
                d = ezr.ydist(tbl, get_label(n))
                if d < best_d:
                    best_d, best_n = d, n
            curr = best_n
        return curr

    strategies = {
        "random": strategy_random,
        "acquire": strategy_acquire,
        "greedy": strategy_greedy
    }
    
    results = {}
    for name, func in strategies.items():
        results[name] = func()
        
    # Determine winner (lowest ydist)
    winner = min(results, key=lambda n: ezr.ydist(tbl, get_label(results[n])))
    
    return {
        "winner": winner,
        "row": results[winner],
        "tried": list(strategies.keys())
    }

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # Mask goals
    temp_tbl = ezr.Tbl([header] + rows)
    goal_indices = [c.at for c in temp_tbl.y]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    def label(i):
        return rows[i]
        
    result = race(header, masked_rows, label)
    print(f"Race Results: The winner is '{result['winner']}' "
          f"which found the best setup at index {result['row']}.")
