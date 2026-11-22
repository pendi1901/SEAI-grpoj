import csv
import random
from step02 import guess

def race(header, rows, label):
    """
    Compares three strategies for finding the best row with a shared 50-label budget.
    1. 'random': Samples 16 rows randomly.
    2. 'newest_pay_rise': Rule of thumb - pick 17 rows with lowest 'YearsAtCompany+' 
       (newest) and highest 'PercentSalaryHike'.
    3. 'model_based': Samples 17 rows with highest predicted 'YearsAtCompany+' 
       using a quick model trained on the first 16 random labels.
    """
    goal_idx = next(i for i, col in enumerate(header) if col.endswith('+') or col.endswith('-'))
    is_maximize = header[goal_idx].endswith('+')
    
    labeled = {}
    def get_label(i):
        if i not in labeled:
            if len(labeled) >= 50:
                raise ValueError("Asked for more than 50 labels")
            labeled[i] = label(i)[0]
        return labeled[i]

    # Strategy 1: Random
    random_indices = random.sample(range(len(rows)), 16)
    
    # Strategy 2: Rule of thumb (Newest staff + high salary hike)
    yac_idx = header.index('YearsAtCompany+')
    hike_idx = header.index('PercentSalaryHike')
    # Sort by newest (low YAC) then high hike
    newest_indices = sorted(range(len(rows)), key=lambda i: (rows[i][yac_idx], -rows[i][hike_idx]))[:17]
    
    # Strategy 3: Model-based (Train on random, predict for rest)
    train_indices = random_indices
    train_rows = []
    for i in train_indices:
        r = list(rows[i])
        r[goal_idx] = get_label(i)
        train_rows.append(r)
    
    test_rows = [list(r) for r in rows]
    for r in test_rows: r[goal_idx] = 0.0
    
    predictions = guess(header, train_rows, test_rows)
    model_indices = sorted(range(len(predictions)), key=lambda i: predictions[i], reverse=is_maximize)[:17]
    
    strategies = {
        "random": random_indices,
        "rule_of_thumb": newest_indices,
        "model_based": model_indices
    }
    
    best_strategy = None
    best_val = float('-inf') if is_maximize else float('inf')
    best_row_idx = -1
    
    for name, indices in strategies.items():
        for idx in indices:
            val = get_label(idx)
            if (is_maximize and val > best_val) or (not is_maximize and val < best_val):
                best_val = val
                best_strategy = name
                best_row_idx = idx
                
    return {"winner": best_strategy, "row": best_row_idx, "tried": list(strategies.keys())}

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rows.append([float(val) if header[i][0].isupper() else val for i, val in enumerate(row)])

    goal_idx = next(i for i, col in enumerate(header) if col.endswith('+') or col.endswith('-'))
    
    def label(i):
        return [rows[i][goal_idx]]

    result = race(header, rows, label)
    
    print("Comparison: Rule of Thumb vs. Data-Driven Search")
    print(f"The winning strategy was: {result['winner']}")
    if result['winner'] == "rule_of_thumb":
        print("The rule of thumb (pay rises to newest) is effective for this data.")
    else:
        print("The model-based approach outperformed the rule of thumb.")
