import csv

def remember(header, rows):
    """
    Identifies staff who stay 'unusually long'.
    We define 'staying long' by the goal columns ending in '+':
    'YearsAtCompany+', 'YearsInCurrentRole+', 'YearsWithCurrManager+'
    We calculate a score based on the sum of these values and return 
    the indices of the top 5% (max 40 rows for 800 records).
    """
    # Identify indices of goal columns ending in '+'
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+')]
    
    scored_rows = []
    for idx, row in enumerate(rows):
        # Calculate score: sum of values in goal columns
        score = sum(row[i] for i in goal_indices)
        scored_rows.append((score, idx))
    
    # Sort by score descending
    scored_rows.sort(key=lambda x: x[0], reverse=True)
    
    # Return top 5% (800 * 0.05 = 40)
    limit = max(1, int(len(rows) * 0.05))
    return [item[1] for item in scored_rows[:limit]]

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
    
    indices = remember(header, rows)
    
    print("Staff members who stay unusually long (Top 5% by tenure metrics):")
    print(f"{'Index':<10} | {'YearsAtCompany':<15} | {'Role':<20}")
    print("-" * 50)
    
    # Find index of relevant columns for display
    idx_comp = header.index('YearsAtCompany+')
    idx_role = header.index('jobRole')
    
    for i in indices:
        print(f"{i:<10} | {rows[i][idx_comp]:<15} | {rows[i][idx_role]:<20}")
