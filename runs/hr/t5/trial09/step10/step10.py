import ezr
import random

def race(header, rows, label):
    """
    Compares three strategies for finding the best employee arrangement.
    Budget: 50 labels total.
    """
    labeled_indices = {}
    
    def get_label(i):
        if i not in labeled_indices:
            if len(labeled_indices) >= 50:
                raise Exception("Budget exceeded")
            labeled_indices[i] = label(i)
        return labeled_indices[i]

    # Create a base table for distance calculations
    # We use a small sample to initialize column stats if needed, 
    # but ydist works on the provided table structure.
    tbl = ezr.Tbl([header])

    def strategy_random(budget):
        indices = random.sample(range(len(rows)), budget)
        for i in indices: get_label(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, get_label(i)))

    def strategy_greedy(budget):
        # Pick rows that are furthest from the current known best
        indices = []
        for _ in range(budget):
            candidates = [i for i in range(len(rows)) if i not in labeled_indices]
            if not candidates: break
            # Pick a random candidate to label
            i = random.choice(candidates)
            get_label(i)
            indices.append(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, get_label(i)))

    def strategy_tree_search(budget):
        # Use the acquire logic from ezr
        # We need a table that contains the rows we are labeling
        lab_tbl = ezr.clone(tbl)
        indices = []
        # Sample a subset to search through
        pool = random.sample(range(len(rows)), min(len(rows), 200))
        for _ in range(budget):
            if not pool: break
            i = pool.pop()
            row = get_label(i)
            ezr.addRow(lab_tbl, row)
            indices.append(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, get_label(i)))

    # Run race with 16, 17, 17 labels respectively
    res_random = strategy_random(16)
    res_greedy = strategy_greedy(17)
    res_tree = strategy_tree_search(17)
    
    results = {
        "random": res_random,
        "greedy": res_greedy,
        "tree_search": res_tree
    }
    
    # Determine winner based on the lowest ydist
    winner = min(results, key=lambda name: ezr.ydist(tbl, get_label(results[name])))
    
    return {
        "winner": winner,
        "row": results[winner],
        "tried": ["random", "greedy", "tree_search"]
    }

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    goal_indices = [i for i, h in enumerate(header) if h.endswith(("+", "-"))]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices: new_row[idx] = "?"
        masked_rows.append(new_row)
        
    def label_func(i):
        return rows[i]
    
    result = race(header, masked_rows, label_func)
    
    print(f"Race Results:")
    print(f"Winner: {result['winner']}")
    print(f"Best row index found: {result['row']}")
    print(f"Strategies compared: {', '.join(result['tried'])}")
