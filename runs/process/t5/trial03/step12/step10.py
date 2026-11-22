import ezr
import random

def race(header, rows, label):
    """
    Compare three strategies for finding the best row within a shared 50-label budget.
    Strategies:
    1. random: Picks rows at random.
    2. greedy: Picks rows based on the best current centroid (using acquire).
    3. tree_search: Uses the tree-based ranker to guide selection.
    """
    budget = 50
    labeled_indices = set()
    
    def oracle_wrapper(idx):
        if idx not in labeled_indices:
            if len(labeled_indices) >= budget:
                raise Exception("Budget exceeded!")
            labeled_indices.add(idx)
        return label(idx)

    # Prepare table for ydist calculations
    # We must ensure the table has the full rows to calculate normalization correctly
    tbl = ezr.Tbl([header] + rows)
    
    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), budget // 3)
        best_idx = -1
        best_ydist = float('inf')
        for i in indices:
            row = oracle_wrapper(i)
            # Use the table to calculate ydist
            d = ezr.ydist(tbl, row)
            if d < best_ydist:
                best_ydist = d
                best_idx = i
        return best_idx, best_ydist

    # Strategy 2: Greedy (using ezr.acquire logic)
    def strategy_greedy():
        subset_budget = budget // 3
        row_to_idx = {id(r): i for i, r in enumerate(rows)}
        
        def local_oracle(r):
            idx = row_to_idx[id(r)]
            true_vals = oracle_wrapper(idx)
            for i in range(len(true_vals)): r[i] = true_vals[i]
            return r
        
        # Acquire returns rows that have been labeled
        labeled = ezr.acquire(tbl, cap=subset_budget, label=local_oracle)
        best_row = min(labeled, key=lambda r: ezr.ydist(tbl, r))
        return row_to_idx[id(best_row)], ezr.ydist(tbl, best_row)

    # Strategy 3: Tree-based Ranker
    def strategy_tree():
        init_size = 5
        indices = random.sample(range(len(rows)), init_size)
        for i in indices: oracle_wrapper(i)
        
        # Create a table of labeled data to train the ranker
        lab_rows = [label(i) for i in labeled_indices]
        lab_tbl = ezr.Tbl([header] + lab_rows)
        ranker = ezr.ranker(lab_tbl)
        
        unlabeled = [i for i in range(len(rows)) if i not in labeled_indices]
        # Pick best based on ranker
        best_idx = min(unlabeled, key=lambda i: ranker(rows[i]))
        row = oracle_wrapper(best_idx)
        
        return best_idx, ezr.ydist(tbl, row)

    results = {
        "random": strategy_random(),
        "greedy": strategy_greedy(),
        "tree_search": strategy_tree()
    }
    
    winner = min(results, key=lambda k: results[k][1])
    return {
        "winner": winner,
        "row": results[winner][0],
        "tried": list(results.keys())
    }

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Keep full rows for the oracle
    full_rows = [list(r) for r in rows]
    
    # Masked rows for the strategies
    goal_indices = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices: new_row[idx] = "?"
        masked_rows.append(new_row)
        
    def label(i):
        return full_rows[i]
    
    random.seed(1234567891)
    result = race(header, masked_rows, label)
    
    print(f"Race Results:")
    print(f"Winner: {result['winner']}")
    print(f"Best row index found: {result['row']}")
    print(f"Strategies tried: {', '.join(result['tried'])}")
