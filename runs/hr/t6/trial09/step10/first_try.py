import ezr
import random

def race(header, rows, label):
    """
    Compare three strategies: random, greedy (nearest neighbor), and tree-based.
    Budget: 50 labels total.
    """
    # Setup
    budget = 50
    labeled_indices = {}
    
    def get_label(i):
        if i not in labeled_indices:
            if len(labeled_indices) >= budget:
                raise Exception("Budget exceeded")
            labeled_indices[i] = label(i)
        return labeled_indices[i]

    # Strategies
    def strategy_random(tbl, masked_rows):
        indices = random.sample(range(len(masked_rows)), budget // 3)
        for i in indices:
            get_label(i)
        return indices

    def strategy_greedy(tbl, masked_rows):
        # Pick rows that are furthest from current knowledge (exploration)
        indices = []
        for _ in range(budget // 3):
            # Simple heuristic: pick index not yet labeled
            candidates = [i for i in range(len(masked_rows)) if i not in labeled_indices]
            if not candidates: break
            i = random.choice(candidates)
            get_label(i)
            indices.append(i)
        return indices

    def strategy_tree(tbl, masked_rows):
        # Use ezr.acquire to get labels
        # We need to map indices for the oracle
        def oracle(row):
            idx = row[-1]
            true_vals = get_label(idx)
            for i, val in enumerate(true_vals):
                row[i] = val
            return row
            
        indexed_rows = [r + [i] for i, r in enumerate(masked_rows)]
        new_header = header + ["_idx"]
        tbl_idx = ezr.Tbl([new_header] + indexed_rows)
        
        labeled = ezr.acquire(tbl_idx, cap=budget // 3, label=oracle)
        return [int(r[-1]) for r in labeled]

    # Run race
    tbl = ezr.Tbl([header] + rows)
    strategies = {
        "random": strategy_random,
        "greedy": strategy_greedy,
        "tree": strategy_tree
    }
    
    results = {}
    for name, func in strategies.items():
        func(tbl, rows)
        # Find best row found by this strategy
        best_idx = -1
        best_ydist = 1e30
        for i in labeled_indices:
            yd = ezr.ydist(tbl, labeled_indices[i])
            if yd < best_ydist:
                best_ydist = yd
                best_idx = i
        results[name] = best_ydist

    winner = min(results, key=results.get)
    
    return {
        "winner": winner,
        "row": [i for i in labeled_indices if ezr.ydist(tbl, labeled_indices[i]) == results[winner]][0],
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
