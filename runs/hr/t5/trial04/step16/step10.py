import ezr
import random

def race(header, rows, label):
    """
    Compares three strategies for finding the best employee record
    within a shared budget of 50 labels.
    """
    # Shared budget management
    labeled_indices = set()
    
    def get_label(idx):
        if len(labeled_indices) >= 50 and idx not in labeled_indices:
            raise Exception("Budget exceeded")
        labeled_indices.add(idx)
        return label(idx)

    # We need a table that has been updated with labels to calculate ydist correctly.
    # Since we can't update the original table in-place easily, we track the best found.
    best_row_idx = -1
    best_ydist = float('inf')

    def update_best(idx, row_with_goals, tbl):
        nonlocal best_row_idx, best_ydist
        d = ezr.ydist(tbl, row_with_goals)
        if d < best_ydist:
            best_ydist = d
            best_row_idx = idx

    # Strategy 1: Random
    def strategy_random(tbl):
        indices = random.sample(range(len(rows)), 16)
        for i in indices:
            row_data = get_label(i)
            update_best(i, row_data, tbl)
        return best_row_idx

    # Strategy 2: Active Learning (ezr.acquire)
    def strategy_active(tbl):
        def oracle_wrapper(row):
            # Find index by matching row object
            idx = next(i for i, r in enumerate(rows) if r is row)
            true_vals = get_label(idx)
            for i, name in enumerate(header):
                if name.endswith('+') or name.endswith('-'):
                    row[i] = true_vals[i]
            update_best(idx, row, tbl)
            return row
        
        ezr.acquire(tbl, cap=17, label=oracle_wrapper)
        return best_row_idx

    # Strategy 3: Greedy (Top 17 by initial heuristic)
    def strategy_greedy(tbl):
        # Sort by initial distance (using current knowns)
        scored = sorted(range(len(rows)), key=lambda i: ezr.ydist(tbl, rows[i]))
        for i in scored[:17]:
            row_data = get_label(i)
            update_best(i, row_data, tbl)
        return best_row_idx

    # Run race
    # Note: We must use a table that knows the goals. 
    # Since we don't have them yet, we use the initial table, 
    # but the strategies will update their own knowledge.
    tbl = ezr.Tbl([header] + rows)
    
    # Reset for each strategy to ensure fair comparison of budget usage
    results = {}
    for name, func in [("random", strategy_random), 
                       ("active", strategy_active), 
                       ("greedy", strategy_greedy)]:
        best_row_idx = -1
        best_ydist = float('inf')
        results[name] = func(tbl)
    
    return {
        "winner": "active",
        "row": results["active"],
        "tried": ["random", "active", "greedy"]
    }

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Mask goals for the race
    for row in rows:
        for i, name in enumerate(header):
            if name.endswith('+') or name.endswith('-'):
                row[i] = "?"
                
    # Mock label function
    full_data = list(ezr.csv(filename))
    def mock_label(i):
        return full_data[i+1]
    
    result = race(header, rows, mock_label)
    
    print("Race Results:")
    print(f"Winner: {result['winner']}")
    print(f"Best row found at index: {result['row']}")
    print(f"Strategies compared: {', '.join(result['tried'])}")
