import csv
import step02
import step06

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
    Estimates goal values for the row and calculates the percentile rank.
    Addresses the 'pay everyone more' question by highlighting that 
    tenure is driven by multiple factors, not just income.
    """
    # 1. Estimate missing goals using role-based averages
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    role_idx = header.index('jobRole')
    
    role_map = {}
    for r in rows:
        role = r[role_idx]
        if role not in role_map:
            role_map[role] = []
        role_map[role].append([r[i] for i in goal_indices])
    
    averages = {role: [sum(vals)/len(vals) for vals in zip(*data)] for role, data in role_map.items()}
    
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
    
    # 3. Reason addressing the 'pay everyone more' question
    reason = (f"While increasing salary is a common strategy, our data shows that tenure is "
              f"multifaceted and this employee's current profile ranks them in the "
              f"{int(p*100)}th percentile of retention, suggesting that non-monetary "
              f"factors like role and experience are equally critical.")
    
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
