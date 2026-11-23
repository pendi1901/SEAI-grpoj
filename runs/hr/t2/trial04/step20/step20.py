import csv
import random
import step01
import step02

def race(header, rows, label):
    """
    Compares the customer's rule of thumb (newest staff get biggest raises)
    against data-driven strategies.
    
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
            if val is not None:
                if best_val is None or (is_maximize and val > best_val) or (not is_maximize and val < best_val):
                    best_val, best_idx = val, i
        return best_idx, best_val

    # Strategy 2: Rule of Thumb (Newest staff = lowest YearsAtCompany+)
    # We define "newest" as the bottom 10% of tenure.
    def strategy_rule_of_thumb():
        yac_idx = header.index("YearsAtCompany+")
        indexed = sorted([(r[yac_idx], i) for i, r in enumerate(rows)])
        # Pick 17 from the newest (lowest tenure)
        indices = [item[1] for item in indexed[:17]]
        best_idx, best_val = -1, None
        for i in indices:
            val = get_label(i)
            if val is not None:
                if best_val is None or (is_maximize and val > best_val) or (not is_maximize and val < best_val):
                    best_val, best_idx = val, i
        return best_idx, best_val

    # Strategy 3: Data-Driven (Top 5% by tenure)
    def strategy_top_percent():
        indices = step01.remember(header, rows)
        sample = random.sample(indices, min(len(indices), 17))
        best_idx, best_val = -1, None
        for i in sample:
            val = get_label(i)
            if val is not None:
                if best_val is None or (is_maximize and val > best_val) or (not is_maximize and val < best_val):
                    best_val, best_idx = val, i
        return best_idx, best_val

    strategies = {
        "random": strategy_random,
        "rule_of_thumb": strategy_rule_of_thumb,
        "data_driven": strategy_top_percent
    }

    results = {}
    for name, func in strategies.items():
        idx, val = func()
        if idx != -1:
            results[name] = {"idx": idx, "val": val}

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
    print(f"Analysis: Is the 'newest staff' rule of thumb effective?")
    print(f"The winning strategy was: {result['winner']}")
    if result['winner'] == 'rule_of_thumb':
        print("Result: Your rule of thumb is effective for this dataset.")
    else:
        print("Result: Data-driven approaches outperformed the rule of thumb.")
