import csv
import random
import step01
import step07

def race(header, rows, label):
    """
    Compare three strategies for finding the best row within a 50-label budget.
    Strategies:
    1. random: Pick 16 random rows.
    2. top_tenure: Pick 17 rows with the highest 'YearsAtCompany+' (using step01 logic).
    3. bottom_tenure: Pick 17 rows with the lowest 'YearsAtCompany+' (as a control).
    """
    goal_idx = -1
    for i, name in enumerate(header):
        if name.endswith('+'):
            goal_idx = i
            break

    # Budget: 50 labels total
    # Strategy 1: Random
    random_indices = random.sample(range(len(rows)), 16)
    
    # Strategy 2: High tenure (using step01 logic)
    # We need to label to find the best, but we only have 50 labels.
    # We will sample 17 from the top 5% of the dataset as a heuristic.
    top_5_percent = step01.remember(header, rows)
    high_tenure_indices = random.sample(top_5_percent, min(17, len(top_5_percent)))
    
    # Strategy 3: Low tenure (control)
    sorted_rows = sorted(range(len(rows)), key=lambda i: rows[i][goal_idx])
    low_tenure_indices = random.sample(sorted_rows[:len(rows)//5], 17)
    
    strategies = {
        "random": random_indices,
        "high_tenure": high_tenure_indices,
        "low_tenure": low_tenure_indices
    }
    
    best_overall_val = -float('inf')
    best_overall_idx = -1
    winner = ""
    
    for name, indices in strategies.items():
        best_strat_val = -float('inf')
        best_strat_idx = -1
        for idx in indices:
            val = label(idx)[0] # Assuming first goal is YearsAtCompany+
            if val > best_strat_val:
                best_strat_val = val
                best_strat_idx = idx
        
        if best_strat_val > best_overall_val:
            best_overall_val = best_strat_val
            best_overall_idx = best_strat_idx
            winner = name
            
    return {"winner": winner, "row": best_overall_idx, "tried": list(strategies.keys())}

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    header = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
        for row in reader:
            new_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    try: new_row.append(float(val))
                    except ValueError: new_row.append(0.0)
                else: new_row.append(val)
            rows.append(new_row)
            
    def label(i):
        return [rows[i][g] for g in goal_indices]
    
    result = race(header, rows, label)
    print(f"The winning strategy is: {result['winner']}")
    print(f"Best row found at index: {result['row']}")
    print(f"Strategies compared: {', '.join(result['tried'])}")
