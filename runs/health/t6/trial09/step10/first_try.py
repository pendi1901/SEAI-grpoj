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
    
    def oracle_wrapper(idx):
        if idx not in labeled_indices:
            if len(labeled_indices) >= budget:
                raise Exception("Budget exceeded")
            labeled_indices.add(idx)
            revealed = label(idx)
            for i, val in enumerate(revealed):
                rows[idx][i] = val
        return rows[idx]

    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), budget // 3)
        for i in indices: oracle_wrapper(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, rows[i]))

    # Strategy 2: Acquire (Active Learning)
    def strategy_acquire():
        tbl_copy = ezr.Tbl([header] + [list(r) for r in rows])
        # We need to pass a label function that works on the index
        labeled = ezr.acquire(tbl_copy, cap=budget // 3, label=lambda r: oracle_wrapper(rows.index(r)))
        return min(range(len(rows)), key=lambda i: ezr.ydist(tbl_copy, rows[i]))

    # Strategy 3: Greedy (Closest to current best)
    def strategy_greedy():
        start_idx = random.choice(range(len(rows)))
        oracle_wrapper(start_idx)
        best_idx = start_idx
        for _ in range((budget // 3) - 1):
            # Find unlabelled row closest to current best
            best_row = rows[best_idx]
            candidates = [i for i in range(len(rows)) if i not in labeled_indices]
            if not candidates: break
            next_idx = min(candidates, key=lambda i: ezr.xdist(tbl, rows[i], best_row))
            oracle_wrapper(next_idx)
            if ezr.ydist(tbl, rows[next_idx]) < ezr.ydist(tbl, rows[best_idx]):
                best_idx = next_idx
        return best_idx

    tbl = ezr.Tbl([header] + rows)
    
    results = {
        "random": strategy_random(),
        "acquire": strategy_acquire(),
        "greedy": strategy_greedy()
    }
    
    winner = min(results, key=lambda k: ezr.ydist(tbl, rows[results[k]]))
    
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
