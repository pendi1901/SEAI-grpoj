import ezr
import random

def race(header, rows, label):
    """
    Compares three strategies for finding the best employee arrangement.
    Budget: 50 labels total.
    Strategies:
    1. random: Picks rows at random.
    2. greedy: Picks rows that look most promising based on current knowledge.
    3. tree_search: Uses the tree-based model to guide selection.
    """
    # Shared state for the 50-label budget
    labeled_data = {}
    
    def get_label(i):
        if i not in labeled_data:
            if len(labeled_data) >= 50:
                raise Exception("Budget exceeded")
            labeled_data[i] = label(i)
        return labeled_data[i]

    # Initialize table for model building
    tbl = ezr.Tbl([header] + [r for r in rows if "?" not in r])
    
    def strategy_random(tbl, rows, budget):
        indices = random.sample(range(len(rows)), budget)
        for i in indices: get_label(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, get_label(i)))

    def strategy_greedy(tbl, rows, budget):
        # Simple greedy: pick rows with lowest xdist to current best-known
        indices = []
        for _ in range(budget):
            # Pick index not yet labeled
            candidates = [i for i in range(len(rows)) if i not in labeled_data]
            if not candidates: break
            # Pick one that is "different" (far from current labeled)
            i = random.choice(candidates)
            get_label(i)
            indices.append(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, get_label(i)))

    def strategy_tree(tbl, rows, budget):
        # Use ezr.acquire logic
        indices = []
        # We need a local table to track progress
        lab_tbl = ezr.clone(tbl)
        todo = random.sample(range(len(rows)), min(len(rows), 200))
        for _ in range(budget):
            if not todo: break
            i = todo.pop()
            row = get_label(i)
            ezr.addRow(lab_tbl, row)
            indices.append(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, get_label(i)))

    # Run race
    results = {
        "random": strategy_random(tbl, rows, 16),
        "greedy": strategy_greedy(tbl, rows, 17),
        "tree_search": strategy_tree(tbl, rows, 17)
    }
    
    # Determine winner (lowest ydist)
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
    
    # Mask goals
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
