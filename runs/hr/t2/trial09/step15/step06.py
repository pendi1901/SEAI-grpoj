import csv
import step02

def get_score(header, row):
    """Calculates a score where higher is better."""
    score = 0
    for i, name in enumerate(header):
        if name.endswith('+'):
            score += row[i]
        elif name.endswith('-'):
            score -= row[i]
    return score

def justify(header, rows, row):
    """
    Estimates goal values for the row, then calculates the percentile
    rank against the provided rows.
    """
    # 1. Estimate missing goals using step02 logic (average by jobRole)
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    role_idx = header.index('jobRole')
    
    # Build averages from full rows
    role_map = {}
    for r in rows:
        role = r[role_idx]
        if role not in role_map:
            role_map[role] = []
        role_map[role].append([r[i] for i in goal_indices])
    
    averages = {role: [sum(vals)/len(vals) for vals in zip(*data)] for role, data in role_map.items()}
    
    # Fill in the "?" values
    target_role = row[role_idx]
    estimates = averages.get(target_role, [0]*len(goal_indices))
    
    filled_row = list(row)
    for i, g_idx in enumerate(goal_indices):
        filled_row[g_idx] = estimates[i]
        
    # 2. Calculate percentile rank
    target_score = get_score(header, filled_row)
    all_scores = [get_score(header, r) for r in rows]
    better_than = sum(1 for s in all_scores if target_score > s)
    p = better_than / len(rows)
    
    reason = f"This employee's estimated tenure metrics rank them in the top {int((1-p)*100)}% of the workforce based on their role as a {target_role}."
    
    return (p, reason)

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
            
    # Test with the first row, masking its goals
    test_row = list(rows[0])
    for i, name in enumerate(header):
        if name.endswith('+') or name.endswith('-'):
            test_row[i] = "?"
            
    p, reason = justify(header, rows, test_row)
    print(f"Percentile: {p:.4f}")
    print(f"Reason: {reason}")
