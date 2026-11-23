import ezr
import random

def race(header, rows, label):
    """
    Compare three strategies for finding the best employee arrangement.
    Budget: 50 labels total.
    """
    # Shared budget tracker
    labeled_indices = {}
    def oracle_wrapper(i):
        if i not in labeled_indices:
            if len(labeled_indices) >= 50:
                raise Exception("Budget exceeded")
            labeled_indices[i] = label(i)
        return labeled_indices[i]

    # Strategies
    def strategy_random(tbl, rows):
        indices = random.sample(range(len(rows)), 50)
        for i in indices: oracle_wrapper(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, rows[i]))

    def strategy_acquire(tbl, rows):
        # Use ezr.acquire logic
        # We need to map the oracle to the index
        def local_oracle(row):
            for i, r in enumerate(rows):
                if r is row: return oracle_wrapper(i)
            return row
        
        labeled = ezr.acquire(tbl, cap=50, label=local_oracle)
        best_row = min(labeled, key=lambda r: ezr.ydist(tbl, r))
        for i, r in enumerate(rows):
            if r is best_row: return i
        return 0

    def strategy_greedy(tbl, rows):
        # Simple greedy: pick one, then pick the one closest to it
        curr = random.randint(0, len(rows)-1)
        oracle_wrapper(curr)
        for _ in range(49):
            # Find unlabelled row closest to current
            best_next = -1
            min_dist = 1e30
            for i in range(len(rows)):
                if i not in labeled_indices:
                    d = ezr.xdist(tbl, rows[i], rows[curr])
                    if d < min_dist:
                        min_dist = d
                        best_next = i
            if best_next == -1: break
            oracle_wrapper(best_next)
            curr = best_next
        return min(labeled_indices.keys(), key=lambda i: ezr.ydist(tbl, rows[i]))

    # Run race
    tbl = ezr.Tbl([header] + rows)
    results = {
        "random": strategy_random(tbl, rows),
        "acquire": strategy_acquire(tbl, rows),
        "greedy": strategy_greedy(tbl, rows)
    }
    
    # Determine winner (lowest ydist)
    winner = min(results, key=lambda k: ezr.ydist(tbl, rows[results[k]]))
    
    return {
        "winner": winner,
        "row": results[winner],
        "tried": list(results.keys())
    }

if __name__ == "__main__":
    data = list(ezr.csv("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"))
    header = data[0]
    rows = data[1:]
    
    # Mask goals
    goal_indices = [i for i, name in enumerate(header) if name[-1] in "+-"]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices: new_row[idx] = "?"
        masked_rows.append(new_row)
        
    def label(i): return rows[i]
    
    result = race(header, masked_rows, label)
    
    print("Strategy Race Results:")
    print(f"Winner: {result['winner']}")
    print(f"Best row found at index: {result['row']}")
    print(f"Strategies compared: {', '.join(result['tried'])}")
    
    exit(0)
