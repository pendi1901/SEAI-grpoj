import ezr
import random

def race(header, rows, label):
    """
    Compares three strategies for finding the best setup:
    1. random: Randomly samples rows.
    2. acquire: Uses the ezr.acquire logic (active learning).
    3. greedy: Picks rows based on proximity to the current best-known configuration.
    """
    budget = 50
    per_strategy = budget // 3
    
    # Track labeled indices to ensure we don't exceed the global budget
    labeled_indices = set()
    
    def oracle_wrapper(row):
        # Find index of the row object in the original list
        idx = rows.index(row)
        if idx not in labeled_indices:
            if len(labeled_indices) >= budget:
                return row
            labeled_indices.add(idx)
            true_vals = label(idx)
            for i, val in enumerate(true_vals):
                row[i] = val
        return row

    # 1. Random Strategy
    random_indices = random.sample(range(len(rows)), per_strategy)
    for i in random_indices:
        oracle_wrapper(rows[i])
    
    # 2. Acquire Strategy
    tbl = ezr.Tbl([header] + rows)
    acq_rows = ezr.acquire(tbl, cap=per_strategy, label=oracle_wrapper)
    
    # 3. Greedy Strategy
    greedy_indices = []
    curr_idx = random.choice(range(len(rows)))
    for _ in range(per_strategy):
        greedy_indices.append(curr_idx)
        oracle_wrapper(rows[curr_idx])
        # Find next best by looking for the closest neighbor in x-space
        curr_idx = min(range(len(rows)), key=lambda i: ezr.xdist(tbl, rows[curr_idx], rows[i]))
    
    # Final evaluation
    final_tbl = ezr.Tbl([header] + rows)
    
    results = {
        "random": min(random_indices, key=lambda i: ezr.ydist(final_tbl, rows[i])),
        "acquire": min([rows.index(r) for r in acq_rows], key=lambda i: ezr.ydist(final_tbl, rows[i])),
        "greedy": min(greedy_indices, key=lambda i: ezr.ydist(final_tbl, rows[i]))
    }
    
    winner = min(results, key=lambda name: ezr.ydist(final_tbl, rows[results[name]]))
    
    return {
        "winner": winner,
        "row": results[winner],
        "tried": ["random", "acquire", "greedy"]
    }

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    original_rows = [list(r) for r in rows]
    
    # Mask goals
    goal_indices = [i for i, h in enumerate(header) if h[-1] in "+-"]
    for row in rows:
        for idx in goal_indices:
            row[idx] = "?"
                
    def label(i):
        return original_rows[i]
    
    outcome = race(header, rows, label)
    
    print(f"Race Results: {outcome}")
    
    # Compare winner vs random baseline
    final_tbl = ezr.Tbl([header] + original_rows)
    winner_score = ezr.ydist(final_tbl, original_rows[outcome['row']])
    random_idx = random.choice(range(len(original_rows)))
    random_score = ezr.ydist(final_tbl, original_rows[random_idx])
    
    print(f"Winner ({outcome['winner']}) ydist: {winner_score:.4f}")
    print(f"Random baseline ydist: {random_score:.4f}")
    
    if winner_score < random_score:
        print("Conclusion: The chosen strategy outperforms random selection.")
    else:
        print("Conclusion: The chosen strategy performed similarly to or worse than random.")
