import ezr
import random
import step07

def race(header, rows, label):
    """
    Compares three strategies: random, greedy (acquisition), and a simple 
    heuristic-based search. Total budget of 50 labels shared.
    """
    budget = 50
    labeled_indices = {}

    def oracle_wrapper(i):
        if i not in labeled_indices:
            if len(labeled_indices) >= budget:
                raise Exception("Budget exceeded")
            labeled_indices[i] = label(i)
        return labeled_indices[i]

    # 1. Random Strategy
    def strategy_random():
        indices = random.sample(range(len(rows)), budget // 3)
        for i in indices: oracle_wrapper(i)
        return min(indices, key=lambda i: ezr.ydist(ezr.Tbl([header] + [rows[i]]), rows[i]))

    # 2. Acquire Strategy (from step07)
    def strategy_acquire():
        # We pass a local wrapper to ensure we track the budget
        return step07.choose(header, rows, oracle_wrapper)

    # 3. Heuristic Strategy (Sort by xdist from centroid, label top)
    def strategy_heuristic():
        tbl = ezr.Tbl([header] + rows)
        mids = ezr.mids(tbl)
        # Sort by xdist (unusual configurations)
        candidates = sorted(range(len(rows)), key=lambda i: ezr.xdist(tbl, rows[i], mids), reverse=True)
        for i in candidates[:budget // 3]:
            oracle_wrapper(i)
        return min(candidates[:budget // 3], key=lambda i: ezr.ydist(tbl, rows[i]))

    results = {
        "random": strategy_random(),
        "acquire": strategy_acquire(),
        "heuristic": strategy_heuristic()
    }

    # Determine winner based on ydist
    tbl = ezr.Tbl([header] + rows)
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
    
    # Mask goals
    for row in rows:
        row[0] = row[1] = row[2] = "?"
        
    def mock_label(i):
        return original_goals[i]
    
    result = race(header, rows, mock_label)
    
    print(f"Race results: The winner is '{result['winner']}' strategy.")
    print(f"Best row found at index {result['row']}.")
    print(f"Strategies compared: {', '.join(result['tried'])}.")
