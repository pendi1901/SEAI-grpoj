import csv
import random
import step01
import step05

def race(header, rows, label):
    """
    Compares three strategies for finding the best row (highest YearsAtCompany+).
    Budget: 50 labels total.
    """
    goal_idx = [i for i, h in enumerate(header) if h.endswith('+')][0]
    
    # Strategy 1: Random
    def strategy_random(budget):
        indices = random.sample(range(len(rows)), budget)
        best_idx = -1
        best_val = -1.0
        for i in indices:
            val = label(i)[0]
            if val > best_val:
                best_val, best_idx = val, i
        return best_idx, best_val

    # Strategy 2: High Tenure Bias (Heuristic)
    def strategy_tenure(budget):
        # Use step01 logic to find top candidates
        candidates = step01.remember(header, rows)
        indices = candidates[:budget]
        best_idx = -1
        best_val = -1.0
        for i in indices:
            val = label(i)[0]
            if val > best_val:
                best_val, best_idx = val, i
        return best_idx, best_val

    # Strategy 3: Driver-based (Heuristic)
    def strategy_drivers(budget):
        # Use step05 logic to find rows that match "good" drivers
        drivers = step05.blame(header, rows)
        # Simple approach: find rows with high values in the top driver column
        col_idx = header.index(drivers[0])
        indexed = sorted([(rows[i][col_idx], i) for i in range(len(rows))], reverse=True)
        indices = [x[1] for x in indexed[:budget]]
        best_idx = -1
        best_val = -1.0
        for i in indices:
            val = label(i)[0]
            if val > best_val:
                best_val, best_idx = val, i
        return best_idx, best_val

    # Execute
    budget_per = 16 # 16 * 3 = 48 <= 50
    res = {}
    
    idx1, val1 = strategy_random(budget_per)
    res["random"] = (val1, idx1)
    
    idx2, val2 = strategy_tenure(budget_per)
    res["tenure_bias"] = (val2, idx2)
    
    idx3, val3 = strategy_drivers(budget_per)
    res["driver_based"] = (val3, idx3)
    
    winner = max(res, key=lambda k: res[k][0])
    
    return {
        "winner": winner,
        "row": res[winner][1],
        "tried": ["random", "tenure_bias", "driver_based"]
    }

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = []
            for i, val in enumerate(row):
                processed.append(float(val) if header[i][0].isupper() else val)
            rows.append(processed)

    goal_idx = [i for i, h in enumerate(header) if h.endswith('+')][0]
    true_data = {i: [rows[i][goal_idx]] for i in range(len(rows))}
    
    # Mask
    for r in rows: r[goal_idx] = "?"
    
    def label(i): return true_data[i]
    
    result = race(header, rows, label)
    print(f"Winner: {result['winner']}")
    print(f"Best row found at index: {result['row']}")
    print(f"Strategies tried: {', '.join(result['tried'])}")
