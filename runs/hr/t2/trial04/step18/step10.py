import csv
import random
import step01

def race(header, rows, label):
    """
    Compares three strategies for finding the best employee row.
    Budget: 50 labels total.
    """
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-'))
    is_maximize = header[goal_idx].endswith('+')
    
    # Track labels used to respect the 50-label budget
    labeled_data = {}
    def get_label(i):
        if i not in labeled_data:
            if len(labeled_data) >= 50:
                return None
            labeled_data[i] = label(i)[0]
        return labeled_data[i]

    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), 16)
        best_idx, best_val = -1, None
        for i in indices:
            val = get_label(i)
            if best_val is None or (is_maximize and val > best_val) or (not is_maximize and val < best_val):
                best_val, best_idx = val, i
        return best_idx, best_val

    # Strategy 2: Top 5% (using step01 logic)
    def strategy_top_percent():
        # step01.remember returns indices based on the full dataset
        indices = step01.remember(header, rows)
        # Sample a subset of these to stay within budget
        sample = random.sample(indices, min(len(indices), 17))
        best_idx, best_val = -1, None
        for i in sample:
            val = get_label(i)
            if best_val is None or (is_maximize and val > best_val) or (not is_maximize and val < best_val):
                best_val, best_idx = val, i
        return best_idx, best_val

    # Strategy 3: Diversity (sample from different parts of the file)
    def strategy_diversity():
        n = len(rows)
        indices = [int(i * (n / 17)) for i in range(17)]
        best_idx, best_val = -1, None
        for i in indices:
            val = get_label(i)
            if best_val is None or (is_maximize and val > best_val) or (not is_maximize and val < best_val):
                best_val, best_idx = val, i
        return best_idx, best_val

    strategies = {
        "random": strategy_random,
        "top_percent": strategy_top_percent,
        "diversity": strategy_diversity
    }

    results = {}
    for name, func in strategies.items():
        idx, val = func()
        results[name] = {"idx": idx, "val": val}

    # Determine winner
    winner = max(results.keys(), key=lambda n: results[n]["val"] if is_maximize else -results[n]["val"])
    
    return {
        "winner": winner,
        "row": results[winner]["idx"],
        "tried": list(strategies.keys())
    }

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-'))
    
    def label(i):
        return [rows[i][goal_idx]]

    result = race(header, rows, label)
    print(f"The winning strategy is: {result['winner']}")
    print(f"Best row found at index: {result['row']}")
    print(f"Strategies tried: {', '.join(result['tried'])}")
