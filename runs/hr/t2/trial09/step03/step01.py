import csv

def remember(header, rows):
    """
    Identifies staff who stay 'unusually long'.
    We define 'staying long' by the goal columns:
    YearsAtCompany+, YearsInCurrentRole+, YearsWithCurrManager+
    We calculate a score for each row based on these maximization goals.
    """
    # Identify indices for goal columns
    goals = []
    for i, name in enumerate(header):
        if name.endswith('+'):
            goals.append(i)
    
    # Calculate scores: sum of normalized values or raw sums
    # Since we want the best (highest) values, we rank by the sum of these columns
    scores = []
    for idx, row in enumerate(rows):
        score = sum(row[i] for i in goals)
        scores.append((score, idx))
    
    # Sort by score descending
    scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return top 5% (800 rows * 0.05 = 40 rows)
    limit = max(1, int(len(rows) * 0.05))
    return [item[1] for item in scores[:limit]]

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            # Convert numeric columns (Uppercase start) to float
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)
    
    best_indices = remember(header, rows)
    
    print("Staff who stay unusually long (Top 5% by tenure metrics):")
    print(f"{'Role':<25} | {'YearsAtCompany':<15} | {'YearsInRole':<15}")
    print("-" * 60)
    
    role_idx = header.index('jobRole')
    yac_idx = header.index('YearsAtCompany+')
    yicr_idx = header.index('YearsInCurrentRole+')
    
    for i in best_indices:
        r = rows[i]
        print(f"{r[role_idx]:<25} | {r[yac_idx]:<15.0f} | {r[yicr_idx]:<15.0f}")
