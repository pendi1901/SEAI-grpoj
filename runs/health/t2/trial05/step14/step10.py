import csv
import random as rnd
import step01

def race(header, rows, label):
    """
    Compares three strategies: random, greedy, and explorer.
    Budget: 50 labels total.
    """
    budget = 50
    labeled_indices = {}

    def get_goals(i):
        if i not in labeled_indices:
            if len(labeled_indices) >= budget:
                raise Exception("Budget exceeded")
            labeled_indices[i] = label(i)
        return labeled_indices[i]

    def score_row(i):
        goals = get_goals(i)
        # MRE- (min), ACC+ (max), PRED40+ (max)
        # Normalize relative to the whole dataset if possible, 
        # but here we just use the raw values for comparison
        mre, acc, pred = goals
        return -mre + acc + pred

    # Strategy 1: Random
    def strategy_random():
        best_idx = -1
        best_s = -float('inf')
        for _ in range(16): # 16 labels
            i = rnd.randint(0, len(rows) - 1)
            s = score_row(i)
            if s > best_s:
                best_s, best_idx = s, i
        return best_idx

    # Strategy 2: Greedy (Sample 16, pick best)
    def strategy_greedy():
        indices = sorted(range(len(rows)), key=lambda i: rows[i][3], reverse=True)[:16]
        best_idx = -1
        best_s = -float('inf')
        for i in indices:
            s = score_row(i)
            if s > best_s:
                best_s, best_idx = s, i
        return best_idx

    # Strategy 3: Explorer (Sample 16, pick based on Min_impurity_decrease)
    def strategy_explorer():
        indices = sorted(range(len(rows)), key=lambda i: rows[i][6])[:16]
        best_idx = -1
        best_s = -float('inf')
        for i in indices:
            s = score_row(i)
            if s > best_s:
                best_s, best_idx = s, i
        return best_idx

    strategies = {
        "random": strategy_random,
        "greedy": strategy_greedy,
        "explorer": strategy_explorer
    }

    results = {}
    for name, func in strategies.items():
        idx = func()
        results[name] = (idx, score_row(idx))

    winner = max(results, key=lambda n: results[n][1])
    return {
        "winner": winner,
        "row": results[winner][0],
        "tried": list(strategies.keys())
    }

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed_row = [val if header[i] == 'criterion' else float(val) 
                                 for i, val in enumerate(row)]
                rows.append(processed_row)
        
        hidden_rows = [["?"] * 3 + r[3:] for r in rows]
        
        def label(i):
            return rows[i][:3]
            
        res = race(header, hidden_rows, label)
        print(f"Winner: {res['winner']}")
        print(f"Best row index found: {res['row']}")
        print(f"Strategies tried: {', '.join(res['tried'])}")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
