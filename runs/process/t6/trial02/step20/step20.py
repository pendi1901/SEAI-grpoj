import ezr
import random

def race(header, rows, label):
    """
    Compare three strategies: 
    1. 'random': Randomly sample rows.
    2. 'big_teams': Always pick the row with the largest 'Team Size'.
    3. 'acquire': Use the tree-based acquisition strategy.
    """
    budget = 50
    labeled_cache = {}

    def oracle_wrapper(idx):
        if idx not in labeled_cache:
            if len(labeled_cache) >= budget:
                raise Exception("Budget exceeded")
            labeled_cache[idx] = label(idx)
        return labeled_cache[idx]

    # Create a base table for distance calculations
    # We must ensure the table is initialized with the full header
    # and that the rows have valid values for ydist to work.
    # Since we only have a budget of 50, we initialize the table
    # with the header and empty rows, then update it as we label.
    tbl = ezr.Tbl([header])

    def get_ydist(idx):
        full_row = oracle_wrapper(idx)
        # Ensure the table knows about this row's goals for normalization
        ezr.addRow(tbl, full_row)
        return ezr.ydist(tbl, full_row)

    # 1. Random Strategy
    def strategy_random():
        indices = random.sample(range(len(rows)), budget // 3)
        return min(indices, key=get_ydist)

    # 2. Big Teams Strategy (Customer's current approach)
    def strategy_big_teams():
        team_size_idx = header.index("Team Size")
        # Sort by team size descending, pick top N
        candidates = sorted(range(len(rows)), key=lambda i: rows[i][team_size_idx], reverse=True)
        return min(candidates[:budget // 3], key=get_ydist)

    # 3. Acquire Strategy
    def strategy_acquire():
        # Re-initialize a local table for the acquire function
        local_tbl = ezr.Tbl([header])
        
        def smart_label(row):
            # Find index of this row in the original list
            idx = rows.index(row)
            full = oracle_wrapper(idx)
            # Update the row in the local table
            for i in range(len(row)): row[i] = full[i]
            ezr.addRow(local_tbl, full)
            return row
            
        # acquire returns a list of rows, we find the best one
        # We pass the original rows to acquire
        labeled = ezr.acquire(local_tbl, cap=budget // 3, label=smart_label)
        best_row = min(labeled, key=lambda r: ezr.ydist(local_tbl, r))
        return rows.index(best_row)

    results = {
        "random": strategy_random(),
        "big_teams": strategy_big_teams(),
        "acquire": strategy_acquire()
    }
    
    winner = min(results, key=lambda name: get_ydist(results[name]))
    
    return {
        "winner": winner,
        "row": results[winner],
        "tried": list(results.keys())
    }

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    header = next(data_gen)
    all_rows = list(data_gen)
    
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    masked_rows = []
    for row in all_rows:
        new_row = list(row)
        for idx in goal_indices: new_row[idx] = "?"
        masked_rows.append(new_row)
        
    def label_func(idx):
        return all_rows[idx]
        
    result = race(header, masked_rows, label_func)
    
    print("Strategy Comparison: Is 'biggest teams' the best approach?")
    print(f"Winner: {result['winner']}")
    print(f"Best row found at index: {result['row']}")
    print(f"Strategies tried: {', '.join(result['tried'])}")
    
    if result['winner'] == 'big_teams':
        print("Conclusion: Your current strategy of using the biggest teams is optimal.")
    else:
        print(f"Conclusion: The '{result['winner']}' strategy outperformed your current 'big_teams' approach.")
        
    exit(0)
