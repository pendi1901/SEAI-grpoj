import ezr
import random
import step01
import step07

def race(header, rows, label):
    """
    Compare three strategies: random, acquire (from ezr), and a greedy search.
    Total budget is 50 labels shared across all strategies.
    """
    # Budget management
    budget = 50
    labeled_indices = set()

    def oracle_wrapper(i):
        if i not in labeled_indices:
            if len(labeled_indices) >= budget:
                raise Exception("Budget exceeded")
            labeled_indices.add(i)
        return label(i)

    # Strategies
    def strategy_random(tbl, budget_per):
        indices = random.sample(range(len(rows)), budget_per)
        return [oracle_wrapper(i) for i in indices]

    def strategy_acquire(tbl, budget_per):
        # Temporarily set the budget for ezr.acquire
        ezr.the.Stop = budget_per
        return ezr.acquire(tbl, cap=budget_per, label=lambda r: oracle_wrapper(rows.index(r)))

    def strategy_greedy(tbl, budget_per):
        # Simple greedy: sample random, then pick the best neighbor
        current = random.choice(rows)
        results = [oracle_wrapper(rows.index(current))]
        for _ in range(budget_per - 1):
            # Look for a row that is closer to the ideal than current
            candidates = random.sample(rows, 10)
            best_c = min(candidates, key=lambda r: ezr.ydist(tbl, r))
            results.append(oracle_wrapper(rows.index(best_c)))
        return results

    # Run race
    strategies = {
        "random": strategy_random,
        "acquire": strategy_acquire,
        "greedy": strategy_greedy
    }
    
    tbl = ezr.Tbl([header] + rows)
    results = {}
    best_overall_ydist = float('inf')
    winner = None
    best_row_idx = -1

    budget_per = budget // len(strategies)
    for name, func in strategies.items():
        labeled = func(tbl, budget_per)
        # Find best in this batch
        for r in labeled:
            d = ezr.ydist(tbl, r)
            if d < best_overall_ydist:
                best_overall_ydist = d
                winner = name
                best_row_idx = rows.index(r)

    return {"winner": winner, "row": best_row_idx, "tried": list(strategies.keys())}

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    rows_gen = ezr.csv(filename)
    header = next(rows_gen)
    rows = list(rows_gen)
    
    # Mask goals
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
    
    def label(i):
        return rows[i]
    
    result = race(header, masked_rows, label)
    
    print("Race Results:")
    print("-" * 30)
    print(f"Winner: {result['winner']}")
    print(f"Best Row Index: {result['row']}")
    print(f"Strategies Tried: {', '.join(result['tried'])}")
    print("-" * 30)
