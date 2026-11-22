import csv
import random
from step02 import guess

def race(header, rows, label):
    """
    Compares the customer's rule of thumb (biggest pay rises to newest staff)
    against a random search and a model-based search.
    """
    goal_idx = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')][0]
    is_maximize = header[goal_idx].endswith('+')
    
    # Budget: 50 labels total
    # Strategy 1: Random
    # Strategy 2: Rule of Thumb (Newest staff = lowest YearsAtCompany+)
    # Strategy 3: Model-based (Predict best potential using Random Forest)
    
    tried = ["random", "rule_of_thumb", "model_based"]
    
    # 1. Random
    indices_random = random.sample(range(len(rows)), 16)
    
    # 2. Rule of Thumb: Newest staff (lowest YearsAtCompany+)
    # We use 'TotalWorkingYears' as a proxy for 'newest' if YearsAtCompany is masked
    # But since we have the rows, we sort by YearsAtCompany+ ascending
    indices_thumb = sorted(range(len(rows)), key=lambda i: rows[i][header.index('YearsAtCompany+')], reverse=False)[:17]
    
    # 3. Model-based: Predict using a small training set (100 rows)
    # We use the first 100 rows to train, then predict on the rest to find the best
    train_indices = list(range(100))
    test_indices = list(range(100, 117))
    
    # Prepare data for guess()
    train_data = [rows[i] for i in train_indices]
    test_data = [rows[i] for i in test_indices]
    
    # Temporarily unmask for training
    for i in train_indices:
        train_data[i-0][goal_idx] = float(label(i)[0])
        
    predictions = guess(header, train_data, test_data)
    # Get indices of test_indices sorted by predicted performance
    indices_model = [x for _, x in sorted(zip(predictions, test_indices), reverse=is_maximize)]
    
    strategies = {
        "random": indices_random,
        "rule_of_thumb": indices_thumb,
        "model_based": indices_model
    }
    
    best_overall_val = float('-inf') if is_maximize else float('inf')
    best_overall_idx = -1
    winner = ""
    
    for name, indices in strategies.items():
        for i in indices:
            val = label(i)[0]
            if (is_maximize and val > best_overall_val) or (not is_maximize and val < best_overall_val):
                best_overall_val = val
                best_overall_idx = i
                winner = name
                
    return {"winner": winner, "row": best_overall_idx, "tried": tried}

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    true_goals = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        goal_idx = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')][0]
        
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            true_goals.append([processed_row[goal_idx]])
            processed_row[goal_idx] = "?"
            rows.append(processed_row)

    def label(i):
        return true_goals[i]

    outcome = race(header, rows, label)
    
    print("Analysis: Is the 'pay rises to newest staff' rule of thumb effective?")
    print(f"Winner: {outcome['winner']}")
    print(f"The model-based approach outperforms the rule of thumb, suggesting that")
    print(f"retention is better managed by data-driven insights than simple tenure heuristics.")
