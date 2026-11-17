import ezr
import random

def race(header, rows, label):
    """
    Compare three strategies for finding the best employee arrangement.
    Strategies:
    1. random: Selects 50 rows at random.
    2. acquire: Uses ezr.acquire (active learning) to find the best.
    3. greedy: Selects the first 50 rows (baseline).
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Define the strategies
    def strategy_random(tbl, cap, label):
        return ezr.grabs(tbl, cap, label)
    
    def strategy_acquire(tbl, cap, label):
        return ezr.acquire(tbl, cap, label)
    
    def strategy_greedy(tbl, cap, label):
        # Simply take the first 'cap' rows
        return [label(rows[i]) for i in range(min(cap, len(rows)))]
    
    strategies = {
        "random": strategy_random,
        "acquire": strategy_acquire,
        "greedy": strategy_greedy
    }
    
    results = {}
    best_overall_ydist = 1e30
    winner = None
    best_row_idx = -1
    
    # Run each strategy
    for name, func in strategies.items():
        # Reset the table for each strategy to ensure fair comparison
        # (though acquire/grabs don't modify the original table)
        labeled = func(tbl, 50, label)
        
        # Find the best row found by this strategy
        best_in_strat = min(labeled, key=lambda r: ezr.ydist(tbl, r))
        dist = ezr.ydist(tbl, best_in_strat)
        
        results[name] = dist
        
        if dist < best_overall_ydist:
            best_overall_ydist = dist
            winner = name
            # Find index in original rows
            best_row_idx = rows.index(best_in_strat)
            
    return {"winner": winner, "row": best_row_idx, "tried": list(strategies.keys())}

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Keep original rows to act as the oracle
    original_rows = [list(r) for r in rows]
    
    # Mask goals
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    def label(i):
        return original_rows[i]
        
    # Run the race
    result = race(header, masked_rows, label)
    
    print("Analysis: Comparing strategies to find the best employee arrangement.")
    print(f"Strategies tested: {', '.join(result['tried'])}")
    print(f"The winning strategy is: {result['winner']}")
    print(f"The best arrangement found is at row index: {result['row']}")
    print("The 'acquire' strategy typically outperforms random selection by focusing")
    print("on the most informative regions of the search space.")
