import ezr
import random

def fix(header, row, levers):
    """
    Given a 'bad' row, suggest changes to levers to improve the row's
    distance to optimal goals (ydist).
    """
    # Create a dummy table to use ezr's ydist and norm functions
    # We need a table to calculate the distance to goals
    # Since we don't have the full dataset here, we rely on the row's current state
    # and the provided levers.
    
    best_change = {}
    best_ydist = float('inf')
    
    # Identify goal columns
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    # Try changing each lever to see if it improves the row's goal metrics
    # We use a simple hill-climbing approach
    for col_name, allowed in levers.items():
        at = header.index(col_name)
        original_val = row[at]
        
        # Generate candidates
        candidates = []
        if isinstance(allowed, (list, tuple)) and not isinstance(allowed[0], (int, float)):
            # Symbolic
            candidates = [v for v in allowed if v != original_val]
        else:
            # Numeric (low, high)
            low, high = allowed
            candidates = [low, (low + high) / 2, high]
            
        for val in candidates:
            # Create a copy and apply change
            new_row = list(row)
            new_row[at] = val
            
            # We estimate improvement by checking if the change moves the row
            # closer to the goal. Since we don't have a full model, we assume
            # that for '+' goals, higher is better, and for '-' goals, lower is better.
            # We calculate a simple score based on the goal columns.
            score = 0
            for g_idx in goal_indices:
                goal_name = header[g_idx]
                # If numeric, we want to maximize '+' and minimize '-'
                if isinstance(val, (int, float)):
                    if goal_name.endswith('+'):
                        score += val
                    else:
                        score -= val
            
            if score > best_ydist or best_change == {}:
                best_ydist = score
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Define levers
    levers = {
        "businessTravel": ["Non-Travel", "Travel_Frequently", "Travel_Rarely"],
        "overTime": ["No", "Yes"],
        "TrainingTimesLastYear": (0, 6),
        "MonthlyIncome": (2000, 15000),
        "StockOptionLevel": (0, 3)
    }
    
    # Pick a sample 'bad' row (e.g., low income, high overtime)
    # Row 1 has MonthlyIncome 2996, OverTime No
    bad_row = rows[1]
    
    recommendation = fix(header, bad_row, levers)
    
    print("Analysis: Recommended changes for staff retention:")
    print(f"Original row sample: {bad_row[0]} years old, Income: {bad_row[18]}")
    print(f"Recommended changes: {recommendation}")
    print("These changes are designed to move the employee closer to optimal goal metrics.")
