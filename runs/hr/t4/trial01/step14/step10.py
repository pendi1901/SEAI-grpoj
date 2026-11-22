import csv
import random
from step02 import guess

def race(header, rows, label):
    """
    Compares three strategies for finding the best row with a shared 50-label budget.
    1. 'random': Samples 16 rows randomly.
    2. 'tenure': Samples 17 rows with highest 'TotalWorkingYears'.
    3. 'income': Samples 17 rows with highest 'MonthlyIncome'.
    """
    goal_idx = next(i for i, col in enumerate(header) if col.endswith('+') or col.endswith('-'))
    is_maximize = header[goal_idx].endswith('+')
    
    # Shared budget tracking
    labeled = {}
    def get_label(i):
        if i not in labeled:
            if len(labeled) >= 50:
                raise ValueError("Asked for more than 50 labels")
            labeled[i] = label(i)[0]
        return labeled[i]

    # Strategy 1: Random
    random_indices = random.sample(range(len(rows)), 16)
    
    # Strategy 2: High Tenure
    tenure_idx = header.index('TotalWorkingYears')
    tenure_indices = sorted(range(len(rows)), key=lambda i: rows[i][tenure_idx], reverse=True)[:17]
    
    # Strategy 3: High Income
    income_idx = header.index('MonthlyIncome')
    income_indices = sorted(range(len(rows)), key=lambda i: rows[i][income_idx], reverse=True)[:17]
    
    # Evaluate all strategies
    strategies = {
        "random": random_indices,
        "tenure": tenure_indices,
        "income": income_indices
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
            processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed_row)

    goal_idx = next(i for i, col in enumerate(header) if col.endswith('+') or col.endswith('-'))
    
    def label(i):
        return [rows[i][goal_idx]]

    result = race(header, rows, label)
    
    print(f"Race Results:")
    print(f"Winner: {result['winner']}")
    print(f"Best row found at index: {result['row']}")
    print(f"Strategies tried: {', '.join(result['tried'])}")
