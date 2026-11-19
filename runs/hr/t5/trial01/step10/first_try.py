import ezr
import random

def race(header, rows, label):
    """
    Compares three strategies for finding the best employee record
    within a shared budget of 50 labels.
    """
    # Shared budget management
    budget = 50
    labeled_cache = {}

    def oracle(row):
        # Find index of row in original list to ensure we don't exceed budget
        # by labeling the same row twice.
        idx = -1
        for i, r in enumerate(rows):
            if r is row:
                idx = i
                break
        
        if idx not in labeled_cache:
            if len(labeled_cache) >= budget:
                raise Exception("Budget exceeded!")
            labeled_cache[idx] = label(row)
        return labeled_cache[idx]

    # Strategies
    def strategy_random(tbl, rows):
        # Randomly sample rows
        samples = random.sample(rows, min(len(rows), budget // 3))
        return [oracle(r) for r in samples]

    def strategy_acquire(tbl, rows):
        # Use ezr's built-in acquire (near best, far from rest)
        return ezr.acquire(tbl, cap=budget // 3, label=oracle)

    def strategy_greedy(tbl, rows):
        # Pick rows that are furthest from the current centroid
        # (Exploration-heavy strategy)
        centroid = ezr.mids(tbl)
        sorted_rows = sorted(rows, key=lambda r: ezr.xdist(tbl, r, centroid), reverse=True)
        return [oracle(r) for r in sorted_rows[:budget // 3]]

    # Run race
    tbl = ezr.Tbl([header] + rows)
    strategies = {
        "random": strategy_random,
        "acquire": strategy_acquire,
        "greedy": strategy_greedy
    }
    
    results = {}
    for name, func in strategies.items():
        labeled = func(tbl, rows)
        # Find best row found by this strategy
        if labeled:
            lab_tbl = ezr.Tbl([header] + labeled)
            best_row = min(labeled, key=lambda r: ezr.ydist(lab_tbl, r))
            results[name] = ezr.ydist(lab_tbl, best_row)
        else:
            results[name] = 1e30

    winner = min(results, key=results.get)
    
    return {
        "winner": winner,
        "row": results[winner],
        "tried": list(strategies.keys())
    }

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    def label_oracle(row):
        # Return the original row from the dataset
        for original_row in rows:
            match = True
            for i in range(len(header)):
                if i not in goal_indices and original_row[i] != row[i]:
                    match = False
                    break
            if match:
                return original_row
        return row

    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    result = race(header, masked_rows, label_oracle)
    
    print("Strategy Race Results:")
    print(f"  Winner: {result['winner']}")
    print(f"  Best ydist found: {result['row']:.4f}")
    print(f"  Strategies compared: {', '.join(result['tried'])}")
