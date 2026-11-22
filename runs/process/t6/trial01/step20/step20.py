import ezr
import random

def race(header, rows, label):
    """
    Compares the customer's current strategy (max team size) against
    random search and the tree-based acquire strategy.
    """
    labeled_indices = {}
    budget_limit = 50

    def oracle_wrapper(i):
        if i not in labeled_indices and len(labeled_indices) < budget_limit:
            labeled_indices[i] = label(i)
        return labeled_indices.get(i, rows[i])

    # We need a table that knows the goal values to calculate ydist.
    # Since we only have partial info, we build a table from the full dataset
    # to get the column statistics (mu, sd) for normalization.
    # We use the original rows to ensure we have valid numeric data for normalization.
    full_tbl = ezr.Tbl([header] + [list(r) for r in rows])
    
    # Helper to score a row using the full_tbl statistics
    def score_row(i):
        # If we have the real row, use it; otherwise, use the row with '?'
        # Note: ydist handles '?' by returning a distance, but normalization 
        # requires numeric values. We use the row from the original data if available.
        row = labeled_indices.get(i, rows[i])
        return ezr.ydist(full_tbl, row)

    # Strategy 1: Random
    def strategy_random(budget):
        indices = random.sample(range(len(rows)), min(budget, budget_limit - len(labeled_indices)))
        for i in indices: oracle_wrapper(i)
        return min(range(len(rows)), key=score_row)

    # Strategy 2: Tree-based (acquire)
    def strategy_tree(budget):
        temp_tbl = ezr.clone(full_tbl, [list(r) for r in rows])
        def local_oracle(row):
            for i, r in enumerate(rows):
                if r is row: return oracle_wrapper(i)
            return row
        ezr.acquire(temp_tbl, cap=len(labeled_indices) + budget, label=local_oracle)
        return min(range(len(rows)), key=score_row)

    # Strategy 3: Customer's Current (Max Team Size)
    # Team Size is at index 8. We pick the rows with the highest Team Size.
    def strategy_customer(budget):
        sorted_indices = sorted(range(len(rows)), key=lambda i: rows[i][8], reverse=True)
        for i in sorted_indices[:budget]:
            oracle_wrapper(i)
        return min(range(len(rows)), key=score_row)

    # Run the race
    budget_per = 16
    results = {
        "random": strategy_random(budget_per),
        "tree": strategy_tree(budget_per),
        "max_team_size": strategy_customer(budget_per)
    }
    
    winner = min(results, key=lambda name: score_row(results[name]))
    
    return {
        "winner": winner,
        "row": results[winner],
        "tried": list(results.keys())
    }

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    try:
        header = next(data_gen)
        all_rows = list(data_gen)
    except StopIteration:
        exit(1)

    test_rows = [row[:] for row in all_rows]
    for row in test_rows:
        row[9] = row[10] = row[11] = "?"

    def label_func(i):
        return all_rows[i]

    outcome = race(header, test_rows, label_func)
    
    print("Comparison: Is 'Max Team Size' better than intelligent search?")
    print(f"Strategies tried: {', '.join(outcome['tried'])}")
    print(f"Winner: {outcome['winner']}")
    
    full_tbl = ezr.Tbl([header] + all_rows)
    dist = ezr.ydist(full_tbl, all_rows[outcome['row']])
    print(f"The winning strategy found a configuration with goal distance: {dist:.4f}")
    
    if outcome['winner'] == "max_team_size":
        print("Result: Your current strategy is optimal.")
    else:
        print("Result: Intelligent search outperforms the 'Max Team Size' strategy.")
    
    exit(0)
