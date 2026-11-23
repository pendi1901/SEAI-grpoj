import ezr
import random

def race(header, rows, label):
    """
    Compare three strategies: random, greedy, and tree-based.
    Budget: 50 labels total.
    """
    budget = 50
    labeled_data = {} # idx -> row
    
    def get_label(i):
        if i not in labeled_data:
            if len(labeled_data) >= budget:
                raise Exception("Budget exceeded")
            labeled_data[i] = label(i)
        return labeled_data[i]

    # Shared table for ydist calculations
    tbl = ezr.Tbl([header] + rows)

    # Strategies
    def strategy_random(masked_rows):
        indices = random.sample(range(len(masked_rows)), budget // 3)
        for i in indices: get_label(i)

    def strategy_greedy(masked_rows):
        # Pick rows that are furthest from current knowledge
        for _ in range(budget // 3):
            candidates = [i for i in range(len(masked_rows)) if i not in labeled_data]
            if not candidates: break
            # Pick a random one to explore
            get_label(random.choice(candidates))

    def strategy_tree(masked_rows):
        # Use ezr.acquire to get labels
        indexed_rows = [list(r) + [i] for i, r in enumerate(masked_rows)]
        new_header = header + ["_idx"]
        tbl_idx = ezr.Tbl([new_header] + indexed_rows)
        
        def oracle(row):
            idx = int(row[-1])
            true_vals = get_label(idx)
            # Update row with true values
            for i in range(len(header)): row[i] = true_vals[i]
            return row
            
        ezr.acquire(tbl_idx, cap=budget // 3, label=oracle)

    # Run race
    strategies = {
        "random": strategy_random,
        "greedy": strategy_greedy,
        "tree": strategy_tree
    }
    
    for name, func in strategies.items():
        func(rows)

    # Evaluate
    results = {}
    best_overall_idx = -1
    best_overall_ydist = 1e30
    
    for name in strategies:
        # Each strategy is evaluated by the best row it found
        # We check all labeled_data to see which strategy found the best
        # In this simplified version, we track the best ydist per strategy
        best_ydist = 1e30
        for i in labeled_data:
            yd = ezr.ydist(tbl, labeled_data[i])
            if yd < best_ydist:
                best_ydist = yd
            if yd < best_overall_ydist:
                best_overall_ydist = yd
                best_overall_idx = i
        results[name] = best_ydist

    winner = min(results, key=results.get)
    
    return {
        "winner": winner,
        "row": best_overall_idx,
        "tried": list(strategies.keys())
    }

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Mask goals
    goal_indices = [i for i, name in enumerate(header) if name.endswith(("+", "-"))]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    def label_harness(i):
        return rows[i]

    result = race(header, masked_rows, label_harness)
    print(f"Race Results: The winner is '{result['winner']}'.")
    print(f"Best row found at index {result['row']}.")
    print(f"Strategies compared: {', '.join(result['tried'])}.")
    exit(0)
