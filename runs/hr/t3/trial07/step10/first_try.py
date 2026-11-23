import csv
import random

def race(header, rows, label):
    """
    Compares three strategies for finding the best row (maximizing '+' goals).
    Budget: 50 labels total.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    def get_score(row):
        # Normalize: for '+', higher is better; for '-', lower is better.
        # Since we only have one goal column in this dataset ('YearsAtCompany+'),
        # we focus on maximizing that.
        return row[goal_indices[0]]

    budget = 50
    tried = ["random", "top_tenure", "high_income"]
    results = {name: {"best_idx": -1, "best_val": -float('inf')} for name in tried}
    
    # Strategy 1: Random
    rand_indices = random.sample(range(len(rows)), 16)
    for i in rand_indices:
        val = get_score(label(i))
        if val > results["random"]["best_val"]:
            results["random"]["best_val"] = val
            results["random"]["best_idx"] = i
            
    # Strategy 2: Top Tenure (Heuristic: look at rows with high Age/TotalWorkingYears)
    # We use 17 labels
    age_idx = header.index('Age')
    sorted_by_age = sorted(range(len(rows)), key=lambda i: rows[i][age_idx], reverse=True)
    for i in sorted_by_age[:17]:
        val = get_score(label(i))
        if val > results["top_tenure"]["best_val"]:
            results["top_tenure"]["best_val"] = val
            results["top_tenure"]["best_idx"] = i
            
    # Strategy 3: High Income (Heuristic: look at rows with high MonthlyIncome)
    # We use 17 labels
    inc_idx = header.index('MonthlyIncome')
    sorted_by_inc = sorted(range(len(rows)), key=lambda i: rows[i][inc_idx], reverse=True)
    for i in sorted_by_inc[:17]:
        val = get_score(label(i))
        if val > results["high_income"]["best_val"]:
            results["high_income"]["best_val"] = val
            results["high_income"]["best_idx"] = i
            
    # Determine winner
    winner = max(tried, key=lambda name: results[name]["best_val"])
    
    return {
        "winner": winner,
        "row": results[winner]["best_idx"],
        "tried": tried
    }

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    header = []
    
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
            
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+'))
    
    # Mask rows
    masked_rows = []
    for row in rows:
        new_row = list(row)
        new_row[goal_idx] = "?"
        masked_rows.append(new_row)
        
    def label(i):
        return rows[i]
        
    outcome = race(header, masked_rows, label)
    
    print(f"Race Results:")
    print(f"Strategies tried: {', '.join(outcome['tried'])}")
    print(f"The winning strategy is: {outcome['winner']}")
    print(f"Best row found at index: {outcome['row']}")
    print(f"Goal value at that row: {rows[outcome['row']][goal_idx]}")
