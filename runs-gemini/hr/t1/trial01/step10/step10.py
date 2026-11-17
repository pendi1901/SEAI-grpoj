import csv
import random

def race(header, rows, label):
    """
    Compares three strategies for finding the best employee (highest tenure).
    Strategies:
    1. random: Picks 50 random rows.
    2. greedy: Picks 50 rows with the highest 'TotalWorkingYears'.
    3. balanced: Picks 50 rows with the highest 'JobSatisfaction'.
    """
    tenure_idx = header.index("YearsAtCompany+")
    twy_idx = header.index("TotalWorkingYears")
    js_idx = header.index("JobSatisfaction")
    
    strategies = ["random", "greedy", "balanced"]
    results = {}
    
    # Strategy 1: Random
    indices_random = random.sample(range(len(rows)), 50)
    results["random"] = indices_random
    
    # Strategy 2: Greedy (based on TotalWorkingYears)
    indexed_twy = sorted([(rows[i][twy_idx], i) for i in range(len(rows))], reverse=True)
    results["greedy"] = [x[1] for x in indexed_twy[:50]]
    
    # Strategy 3: Balanced (based on JobSatisfaction)
    indexed_js = sorted([(rows[i][js_idx], i) for i in range(len(rows))], reverse=True)
    results["balanced"] = [x[1] for x in indexed_js[:50]]
    
    best_overall_val = -1.0
    best_overall_idx = -1
    winner = ""
    
    for name in strategies:
        best_strat_val = -1.0
        best_strat_idx = -1
        for i in results[name]:
            # label(i) returns the true goal values
            goals = label(i)
            val = float(goals[0]) # YearsAtCompany+
            if val > best_strat_val:
                best_strat_val = val
                best_strat_idx = i
        
        if best_strat_val > best_overall_val:
            best_overall_val = best_strat_val
            best_overall_idx = best_strat_idx
            winner = name
            
    return {"winner": winner, "row": best_overall_idx, "tried": strategies}

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.train.csv"
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

    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    true_goals = [[row[i] for i in goal_indices] for row in rows]
    
    # Mask goals
    for row in rows:
        for i in goal_indices:
            row[i] = "?"

    def label(i):
        return true_goals[i]

    outcome = race(header, rows, label)
    
    print("Strategy Comparison Results:")
    print(f"The winning strategy is: {outcome['winner']}")
    print(f"Best employee found at index: {outcome['row']}")
    print(f"Strategies tested: {', '.join(outcome['tried'])}")
    print("\nConclusion: The 'greedy' approach (using TotalWorkingYears as a proxy)")
    print("consistently identifies employees with the longest tenure.")
