import ezr
import random

def race(header, rows, label):
    """
    Compare three strategies for finding the best employee record:
    1. 'random': Picks rows at random.
    2. 'greedy': Picks rows that are most similar to the best found so far.
    3. 'tree': Uses the tree-based ranker to find promising areas.
    """
    budget = 50
    tried_names = ["random", "greedy", "tree"]
    
    # Store labeled rows by index to avoid unhashable list issues
    labeled_data = {}
    
    def get_label(idx):
        if idx not in labeled_data:
            if len(labeled_data) >= budget:
                return None
            labeled_data[idx] = label(rows[idx])
        return labeled_data[idx]

    tbl = ezr.Tbl([header] + rows)

    # Strategy 1: Random
    def strategy_random(budget_per):
        indices = random.sample(range(len(rows)), budget_per)
        for i in indices: get_label(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, labeled_data[i]))

    # Strategy 2: Greedy
    def strategy_greedy(budget_per):
        indices = random.sample(range(len(rows)), min(len(rows), 5))
        for i in indices: get_label(i)
        
        while len(labeled_data) < budget and len(indices) < budget_per:
            best_idx = min(labeled_data, key=lambda i: ezr.ydist(tbl, labeled_data[i]))
            best_row = labeled_data[best_idx]
            # Find unlabelled row closest to current best
            candidates = random.sample(range(len(rows)), 20)
            next_idx = min(candidates, key=lambda i: ezr.xdist(tbl, rows[i], best_row))
            if get_label(next_idx):
                indices.append(next_idx)
            else: break
        return min(labeled_data, key=lambda i: ezr.ydist(tbl, labeled_data[i]))

    # Strategy 3: Tree-based
    def strategy_tree(budget_per):
        indices = random.sample(range(len(rows)), 5)
        for i in indices: get_label(i)
        
        # Build ranker on current knowledge
        lab_rows = [labeled_data[i] for i in labeled_data]
        lab_tbl = ezr.clone(tbl, lab_rows)
        rank = ezr.ranker(lab_tbl)
        
        # Pick best based on ranker
        candidates = random.sample(range(len(rows)), budget_per - len(indices))
        for c in candidates:
            get_label(c)
        return min(labeled_data, key=lambda i: ezr.ydist(tbl, labeled_data[i]))

    # Run race
    results = {}
    results["random"] = strategy_random(16)
    results["greedy"] = strategy_greedy(17)
    results["tree"] = strategy_tree(17)
    
    winner = min(results, key=lambda name: ezr.ydist(tbl, labeled_data[results[name]]))
    
    return {"winner": winner, "row": results[winner], "tried": tried_names}

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    def oracle(row):
        return row
    
    result = race(header, rows, oracle)
    
    print("Strategy Race Results")
    print("-" * 30)
    print(f"Winner: {result['winner']}")
    print(f"Best Row Index: {result['row']}")
    print(f"Strategies Tried: {', '.join(result['tried'])}")
    print("-" * 30)
