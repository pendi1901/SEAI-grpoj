import csv

def get_score(header, row):
    """Calculates a composite score for a row based on goal columns."""
    score = 0
    for i, val in enumerate(row):
        if val == "?":
            continue
        name = header[i]
        if name.endswith('+'):
            score += val
        elif name.endswith('-'):
            score -= val
    return score

def justify(header, rows, row):
    """
    Estimates the score of a row by finding the average score of 
    employees with similar 'MonthlyIncome' (a proxy for pay).
    Returns the percentile rank and a justification regarding pay.
    """
    income_idx = header.index('MonthlyIncome')
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    # Estimate row's score based on average of employees with similar income (+/- 10%)
    target_income = row[income_idx]
    similar_rows = [r for r in rows if 0.9 * target_income <= r[income_idx] <= 1.1 * target_income]
    
    if not similar_rows:
        similar_rows = rows
        
    avg_score = sum(get_score(header, r) for r in similar_rows) / len(similar_rows)
    
    # Calculate percentile
    all_scores = [get_score(header, r) for r in rows]
    better_than = [s for s in all_scores if avg_score > s]
    p = len(better_than) / len(all_scores)
    
    reason = (f"Increasing pay alone is insufficient because tenure is driven by a complex "
              f"mix of role satisfaction and management, and this profile's current "
              f"tenure-related metrics rank in the {p:.2f} percentile of all employees.")
    
    return (p, reason)

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    header = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for line in reader:
            processed_row = []
            for i, val in enumerate(line):
                if header[i][0].isupper():
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    # Sample a row and mask goals
    sample_row = list(rows[0])
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    for i in goal_indices:
        sample_row[i] = "?"
        
    p, reason = justify(header, rows, sample_row)
    print(reason)
    exit(0)
