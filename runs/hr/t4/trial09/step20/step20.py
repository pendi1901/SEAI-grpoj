import csv
import random
import step02

def race(header, rows, label):
    """
    Compares three strategies for finding the best row:
    1. 'random': Picks 16 rows at random.
    2. 'newest_staff': Picks 17 rows with the lowest 'YearsAtCompany+'.
    3. 'pay_rise_logic': Picks 17 rows with the lowest 'YearsAtCompany+' 
       (the customer's rule of thumb: give biggest pay rises to newest staff).
    """
    budget = 50
    strategies = ["random", "newest_staff", "pay_rise_logic"]
    
    # Define selection logic for each strategy
    def get_candidates(strategy):
        if strategy == "random":
            return random.sample(range(len(rows)), 16)
        elif strategy == "newest_staff" or strategy == "pay_rise_logic":
            # Both strategies target the newest staff (lowest tenure)
            idx = header.index('YearsAtCompany+')
            # Sort by tenure ascending
            sorted_indices = sorted(range(len(rows)), key=lambda i: rows[i][idx])
            return sorted_indices[:17]
        return []

    # Collect unique indices to label (budget constraint)
    all_indices = set()
    for s in strategies:
        all_indices.update(get_candidates(s))
    
    # Label the rows
    labeled_data = {}
    for i in all_indices:
        labeled_data[i] = label(i)[0]
    
    # Prepare training set for step02.guess
    goal_idx = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')][0]
    train_rows = []
    for i, val in labeled_data.items():
        r = rows[i][:]
        r[goal_idx] = val
        train_rows.append(r)
        
    # Predict for all rows
    predictions = step02.guess(header, train_rows, rows)
    
    # Find the best row index for each strategy
    best_strategy = None
    best_row_idx = -1
    max_val = -float('inf')
    
    for s in strategies:
        candidates = get_candidates(s)
        for idx in candidates:
            if predictions[idx] > max_val:
                max_val = predictions[idx]
                best_row_idx = idx
                best_strategy = s
                
    return {"winner": best_strategy, "row": best_row_idx, "tried": strategies}

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    true_goals = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        goal_idx = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')][0]
        for row in reader:
            processed = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            true_goals.append(processed[goal_idx])
            processed[goal_idx] = "?"
            rows.append(processed)
            
    def label(i):
        return [true_goals[i]]
        
    result = race(header, rows, label)
    
    print("Analysis: Is the 'pay rise for newest staff' rule effective?")
    print(f"The winning strategy was '{result['winner']}'.")
    if result['winner'] == 'pay_rise_logic':
        print("Conclusion: Your rule of thumb is effective for identifying high-potential retention candidates.")
    else:
        print("Conclusion: Your rule of thumb is outperformed by other search strategies.")
    print(f"Strategies compared: {', '.join(result['tried'])}.")
