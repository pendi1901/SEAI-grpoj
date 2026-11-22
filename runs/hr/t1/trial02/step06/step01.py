import csv

def remember(header, rows):
    """
    Identifies staff who stay 'unusually long'.
    We define 'staying long' by the goal columns ending in '+':
    'YearsAtCompany+', 'YearsInCurrentRole+', 'YearsWithCurrManager+'
    We calculate a score based on the sum of these values and return the top 5%.
    """
    # Identify indices for goal columns ending in '+'
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+')]
    
    scored_rows = []
    for idx, row in enumerate(rows):
        # Calculate score: sum of values in goal columns
        score = sum(row[i] for i in goal_indices)
        scored_rows.append((score, idx))
    
    # Sort by score descending (higher is better)
    scored_rows.sort(key=lambda x: x[0], reverse=True)
    
    # Return top 5% (800 rows * 0.05 = 40 rows)
    limit = max(1, int(len(rows) * 0.05))
    return [item[1] for item in scored_rows[:limit]]

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    header = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            # Convert numeric columns (starting with uppercase) to float
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    best_indices = remember(header, rows)
    
    print(f"Found {len(best_indices)} employees with unusually long tenure.")
    print("Top records (Index, YearsAtCompany, YearsInCurrentRole, YearsWithCurrManager):")
    for idx in best_indices:
        row = rows[idx]
        # Indices for the specific goal columns
        yac = row[header.index('YearsAtCompany+')]
        yicr = row[header.index('YearsInCurrentRole+')]
        ywcm = row[header.index('YearsWithCurrManager+')]
        print(f"Row {idx}: {yac} years at company, {yicr} in role, {ywcm} with manager")
