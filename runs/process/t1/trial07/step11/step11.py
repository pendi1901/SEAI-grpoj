import csv

def remember(header, rows):
    """
    Identifies the top 5% of rows based on goal performance.
    Goals ending in '-' are minimized, '+' are maximized.
    """
    goal_indices = []
    for i, name in enumerate(header):
        if name.endswith('-') or name.endswith('+'):
            goal_indices.append((i, name[-1]))

    def get_score(row):
        # Normalize goals to a 0-1 scale and aggregate
        # Since we want to minimize '-' and maximize '+',
        # we treat all as minimization: val for '-', (1-val) for '+'
        score = 0.0
        for idx, op in goal_indices:
            val = float(row[idx])
            if op == '-':
                score += val
            else:
                score += (1.0 - val)
        return score

    # Calculate scores for all rows
    scored = []
    for i, row in enumerate(rows):
        scored.append((get_score(row), i))
    
    # Sort by score ascending (lower is better)
    scored.sort(key=lambda x: x[0])
    
    # Return top 5% (or at least 1)
    limit = max(1, len(rows) // 20)
    return [item[1] for item in scored[:limit]]

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                # Convert numeric columns to float
                processed_row = []
                for val in row:
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)
        
        best_indices = remember(header, rows)
        
        print("Customer Inquiry: Top Performing Historical Setups")
        print("-" * 50)
        print(f"Identified {len(best_indices)} top-performing configurations.")
        print("These setups represent the best outcomes in our historical data.")
        print("\nSample of top-tier setups:")
        for idx in best_indices[:3]:
            print(f"Row {idx}: {rows[idx]}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
