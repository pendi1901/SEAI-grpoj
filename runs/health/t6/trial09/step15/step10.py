import ezr
import random

def race(header, rows, label):
    """
    Compare three strategies for finding the best setup within a 50-label budget.
    Strategies:
    1. random: Randomly samples rows.
    2. acquire: Uses ezr.acquire (model-based active learning).
    3. greedy: Picks the next row by finding the one closest to the current best.
    """
    budget = 50
    labeled_indices = set()
    
    # Helper to ensure we only label up to 50 unique rows
    def oracle_wrapper(idx):
        if idx not in labeled_indices:
            if len(labeled_indices) >= budget:
                return rows[idx]
            labeled_indices.add(idx)
            revealed = label(idx)
            for i, val in enumerate(revealed):
                rows[idx][i] = val
        return rows[idx]

    # We need a reference table for ydist calculations. 
    # Since we can't calculate ydist on '?', we only evaluate rows that have been labeled.
    def get_ydist(row):
        # If goals are still '?', we can't calculate ydist. Return a high value.
        if any(isinstance(row[c.at], str) and row[c.at] == "?" for c in tbl.y):
            return 1e30
        return ezr.ydist(tbl, row)

    tbl = ezr.Tbl([header] + rows)

    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), budget // 3)
        for i in indices: oracle_wrapper(i)
        return min(range(len(rows)), key=lambda i: get_ydist(rows[i]))

    # Strategy 2: Acquire
    def strategy_acquire():
        # ezr.acquire returns rows that have been labeled.
        # We use the original rows list to ensure updates are reflected.
        ezr.acquire(tbl, cap=budget // 3, label=lambda r: oracle_wrapper(rows.index(r)))
        return min(range(len(rows)), key=lambda i: get_ydist(rows[i]))

    # Strategy 3: Greedy
    def strategy_greedy():
        start_idx = random.choice(range(len(rows)))
        oracle_wrapper(start_idx)
        best_idx = start_idx
        for _ in range((budget // 3) - 1):
            best_row = rows[best_idx]
            candidates = [i for i in range(len(rows)) if i not in labeled_indices]
            if not candidates: break
            # Find unlabelled row closest to current best in X-space
            next_idx = min(candidates, key=lambda i: ezr.xdist(tbl, rows[i], best_row))
            oracle_wrapper(next_idx)
            if get_ydist(rows[next_idx]) < get_ydist(rows[best_idx]):
                best_idx = next_idx
        return best_idx

    results = {
        "random": strategy_random(),
        "acquire": strategy_acquire(),
        "greedy": strategy_greedy()
    }
    
    # Winner is the one with the lowest ydist
    winner = min(results, key=lambda k: get_ydist(rows[results[k]]))
    
    return {
        "winner": winner,
        "row": results[winner],
        "tried": ["random", "acquire", "greedy"]
    }

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    all_rows = data[1:]
    
    # Mask goals
    goal_indices = [i for i, name in enumerate(header) if name[-1] in "+-"]
    masked_rows = []
    for row in all_rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    def label_func(i):
        return all_rows[i]
        
    result = race(header, masked_rows, label_func)
    
    print(f"Race complete. Winner: {result['winner']}")
    print(f"Best row found at index: {result['row']}")
    print(f"Strategies tried: {', '.join(result['tried'])}")
    exit(0)
