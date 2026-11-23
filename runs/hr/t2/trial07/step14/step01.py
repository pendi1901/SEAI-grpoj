import csv

def remember(header, rows):
    """
    Identifies staff who stay 'unusually long'.
    We define 'staying long' by maximizing the goal-oriented columns:
    'YearsAtCompany+', 'YearsInCurrentRole+', and 'YearsWithCurrManager+'.
    We calculate a score based on the sum of these normalized values.
    """
    # Identify indices for goal columns
    idx_at_company = header.index('YearsAtCompany+')
    idx_in_role = header.index('YearsInCurrentRole+')
    idx_with_manager = header.index('YearsWithCurrManager+')

    # Calculate scores for each row
    scores = []
    for i, row in enumerate(rows):
        # Sum the values of the goal columns
        score = row[idx_at_company] + row[idx_in_role] + row[idx_with_manager]
        scores.append((score, i))

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
            # Convert numeric columns (starting with uppercase) to float
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    best_indices = remember(header, rows)
    
    print("Staff records with unusually long tenure (Top 5%):")
    print(f"{'Index':<10} | {'YearsAtCompany':<15} | {'Role':<20}")
    print("-" * 50)
    
    idx_at = header.index('YearsAtCompany+')
    idx_role = header.index('jobRole')
    
    for i in best_indices:
        print(f"{i:<10} | {rows[i][idx_at]:<15} | {rows[i][idx_role]:<20}")
