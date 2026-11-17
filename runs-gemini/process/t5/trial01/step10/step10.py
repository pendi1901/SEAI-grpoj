import ezr
import random

def race(header, rows, label):
    """
    Compares three strategies for finding the best row:
    1. random: Picks 50 rows at random.
    2. acquire: Uses the library's active learning acquisition.
    3. greedy: Picks the first 50 rows and labels them (baseline).
    """
    # Budget is 50 labels total across all strategies
    # We allocate 50 labels per strategy to compare their effectiveness
    # within the same budget constraint.
    
    def get_best(labeled_rows, tbl):
        return min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))

    tbl = ezr.Tbl([header] + rows)
    
    # Strategy 1: Random
    random_rows = random.sample(rows, 50)
    labeled_random = [label(r) for r in random_rows]
    best_random = get_best(labeled_random, tbl)
    
    # Strategy 2: Acquire (Active Learning)
    # We use the library's acquire function
    ezr.the.Stop = 50
    labeled_acquire = ezr.acquire(tbl, cap=50, label=label)
    best_acquire = get_best(labeled_acquire, tbl)
    
    # Strategy 3: Greedy (First 50)
    greedy_rows = rows[:50]
    labeled_greedy = [label(r) for r in greedy_rows]
    best_greedy = get_best(labeled_greedy, tbl)
    
    # Compare results
    results = {
        "random": ezr.ydist(tbl, best_random),
        "acquire": ezr.ydist(tbl, best_acquire),
        "greedy": ezr.ydist(tbl, best_greedy)
    }
    
    winner = min(results, key=results.get)
    
    # Find the index of the best row found by the winner
    best_row = None
    if winner == "random": best_row = best_random
    elif winner == "acquire": best_row = best_acquire
    else: best_row = best_greedy
    
    best_idx = -1
    for i, r in enumerate(rows):
        if r == best_row:
            best_idx = i
            break
            
    return {
        "winner": winner,
        "row": best_idx,
        "tried": ["random", "acquire", "greedy"]
    }

if __name__ == "__main__":
    filename = "pom3a.train.csv"
    rows_iter = ezr.csv(filename)
    header = next(rows_iter)
    all_rows = list(rows_iter)
    
    # The oracle returns the full row data
    def oracle(row):
        return row
    
    # Run the race
    result = race(header, all_rows, oracle)
    
    print("Race Results:")
    print(f"The winning strategy is: {result['winner']}")
    print(f"Best row found at index: {result['row']}")
    print(f"Strategies compared: {', '.join(result['tried'])}")
    
    exit(0)
