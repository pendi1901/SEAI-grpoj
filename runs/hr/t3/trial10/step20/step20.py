import csv
import random

def race(header, rows, label):
    """
    Compares the customer's rule of thumb (newest staff) against other strategies
    to see which finds the highest 'YearsAtCompany+' (maximize).
    Budget: 50 labels total.
    """
    # Identify the goal column index
    goal_idx = next(i for i, h in enumerate(header) if h.endswith('+'))
    
    # Strategies:
    # 1. random: Pick 16 random rows.
    # 2. rule_of_thumb: Pick 17 newest staff (lowest TotalWorkingYears).
    # 3. tenure_focus: Pick 17 most experienced staff (highest TotalWorkingYears).
    
    strategies = ["random", "rule_of_thumb", "tenure_focus"]
    indices = range(len(rows))
    
    # Pre-calculate indices for strategies
    # 'TotalWorkingYears' is a reliable proxy for tenure/newness
    tenure_idx = header.index('TotalWorkingYears')
    
    # Newest = lowest total working years
    newest_sorted = sorted(indices, key=lambda i: rows[i][tenure_idx])
    # Most experienced = highest total working years
    experienced_sorted = sorted(indices, key=lambda i: rows[i][tenure_idx], reverse=True)
    
    selection = {
        "random": random.sample(indices, 16),
        "rule_of_thumb": newest_sorted[:17],
        "tenure_focus": experienced_sorted[:17]
    }
    
    best_overall_val = -float('inf')
    best_overall_idx = -1
    strategy_bests = {name: -float('inf') for name in strategies}
    
    # Evaluate
    for name in strategies:
        for idx in selection[name]:
            full_row = label(idx)
            # Ensure we access the goal column correctly
            val = float(full_row[goal_idx])
            
            if val > strategy_bests[name]:
                strategy_bests[name] = val
            
            if val > best_overall_val:
                best_overall_val = val
                best_overall_idx = idx
    
    winner = max(strategy_bests, key=strategy_bests.get)
                
    return {"winner": winner, "row": best_overall_idx, "tried": strategies}

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
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    goal_idx = next(i for i, h in enumerate(header) if h.endswith('+'))
    true_goals = [r[goal_idx] for r in rows]
    
    # Mask goals in the rows list
    for r in rows:
        r[goal_idx] = "?"

    def label(i):
        # Return a copy of the row with the true goal value restored
        row_copy = rows[i][:]
        row_copy[goal_idx] = true_goals[i]
        return row_copy

    result = race(header, rows, label)
    
    print("Comparison: Is the 'newest staff' rule of thumb effective?")
    print(f"Winner Strategy: {result['winner']}")
    print("The 'rule_of_thumb' strategy (targeting newest staff) was compared against")
    print("random sampling and targeting high-tenure staff.")
    if result['winner'] == 'rule_of_thumb':
        print("Conclusion: Your rule of thumb is effective for finding high-tenure outcomes.")
    else:
        print("Conclusion: Your rule of thumb is outperformed by other strategies.")
