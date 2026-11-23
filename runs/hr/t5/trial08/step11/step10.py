import ezr
import random

def race(header, rows, label):
    """
    Compare three strategies for finding the best employee arrangement.
    Budget: 50 labels total.
    """
    # Shared budget tracker
    labeled_data = {}
    
    def oracle_wrapper(i):
        if i not in labeled_data:
            if len(labeled_data) >= 50:
                return None
            labeled_data[i] = label(i)
        return labeled_data[i]

    # We need a table that knows the true goal values to calculate ydist.
    # Since we only have 50 labels, we build a 'lab' table from those.
    # To calculate ydist, we need a table that has seen the full distribution.
    # We use the initial rows to build the column definitions.
    full_tbl = ezr.Tbl([header] + rows)

    def get_ydist(row_idx):
        # If we haven't labeled this row, we can't calculate its true ydist.
        # We return a high value for unlabelled rows to discourage picking them
        # as the 'best' unless they are labeled.
        if row_idx not in labeled_data:
            return 1e30
        return ezr.ydist(full_tbl, labeled_data[row_idx])

    # Strategies
    def strategy_random(rows):
        indices = random.sample(range(len(rows)), 16) # 16 * 3 = 48 < 50
        for i in indices: oracle_wrapper(i)
        return min(indices, key=get_ydist)

    def strategy_acquire(rows):
        # Use ezr.acquire logic
        # We need to map the oracle to the index
        def local_oracle(row):
            for i, r in enumerate(rows):
                if r is row: return oracle_wrapper(i)
            return row
        
        # We use a subset of the budget
        labeled = ezr.acquire(full_tbl, cap=17, label=local_oracle)
        # Find index of best labeled row
        best_row = min(labeled, key=lambda r: ezr.ydist(full_tbl, r))
        for i, r in enumerate(rows):
            if r is best_row: return i
        return 0

    def strategy_greedy(rows):
        # Simple greedy: pick one, then pick the one closest to it
        curr = random.randint(0, len(rows)-1)
        oracle_wrapper(curr)
        for _ in range(16):
            best_next = -1
            min_dist = 1e30
            for i in range(len(rows)):
                if i not in labeled_data:
                    d = ezr.xdist(full_tbl, rows[i], rows[curr])
                    if d < min_dist:
                        min_dist = d
                        best_next = i
            if best_next == -1: break
            oracle_wrapper(best_next)
            curr = best_next
        return min(labeled_data.keys(), key=get_ydist)

    # Run race
    results = {
        "random": strategy_random(rows),
        "acquire": strategy_acquire(rows),
        "greedy": strategy_greedy(rows)
    }
    
    # Determine winner (lowest ydist)
    winner = min(results, key=lambda k: get_ydist(results[k]))
    
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
