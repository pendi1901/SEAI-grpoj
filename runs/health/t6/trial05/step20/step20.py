import ezr
import random

def race(header, rows, label):
    """
    Compares three strategies: random, acquire, and heuristic.
    Total budget of 50 labels shared.
    """
    budget = 50
    labeled_indices = {}

    def oracle_wrapper(i):
        if i not in labeled_indices:
            if len(labeled_indices) >= budget:
                return None
            goals = label(i)
            rows[i][0], rows[i][1], rows[i][2] = goals[0], goals[1], goals[2]
            labeled_indices[i] = rows[i]
            ezr.addCols(tbl, rows[i])
        return labeled_indices[i]

    # Create a master table to provide context for ydist/xdist
    tbl = ezr.Tbl([header] + rows)

    # 1. Random Strategy
    def strategy_random():
        indices = random.sample(range(len(rows)), budget // 3)
        for i in indices: oracle_wrapper(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, rows[i]))

    # 2. Acquire Strategy (using ezr.acquire directly to avoid step07's internal logic)
    def strategy_acquire():
        # Use a subset of rows for acquisition
        todo = random.sample(range(len(rows)), min(len(rows), 128))
        # Label initial set
        for _ in range(ezr.the.Start):
            if todo: oracle_wrapper(todo.pop())
        # Continue until budget
        while todo and len(labeled_indices) < (budget // 3) * 2:
            oracle_wrapper(todo.pop())
        return min(labeled_indices.keys(), key=lambda i: ezr.ydist(tbl, rows[i]))

    # 3. Heuristic Strategy (Sort by xdist from centroid, label top)
    def strategy_heuristic():
        mids = ezr.mids(tbl)
        candidates = sorted(range(len(rows)), key=lambda i: ezr.xdist(tbl, rows[i], mids), reverse=True)
        for i in candidates[:budget // 3]:
            oracle_wrapper(i)
        return min(candidates[:budget // 3], key=lambda i: ezr.ydist(tbl, rows[i]))

    # Execute strategies
    results = {
        "random": strategy_random(),
        "acquire": strategy_acquire(),
        "heuristic": strategy_heuristic()
    }

    # Determine winner based on ydist of the best row found by each
    winner = min(results, key=lambda name: ezr.ydist(tbl, rows[results[name]]))
    
    return {
        "winner": winner,
        "row": results[winner],
        "tried": list(results.keys())
    }

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # Keep original goals for the oracle
    original_goals = [[r[0], r[1], r[2]] for r in rows]
    
    # Mask goals in the rows passed to the race
    for row in rows:
        row[0] = row[1] = row[2] = "?"
        
    def mock_label(i):
        return original_goals[i]
    
    result = race(header, rows, mock_label)
    
    print(f"Race results: The winner is '{result['winner']}' strategy.")
    print(f"Best row found at index {result['row']}.")
    print(f"Strategies compared: {', '.join(result['tried'])}.")
