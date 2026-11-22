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

    def score_row(row):
        # Normalize goals: 
        # For '-', lower is better. For '+', higher is better (1 - val).
        total = 0.0
        for idx, op in goal_indices:
            val = float(row[idx])
            total += val if op == '-' else (1.0 - val)
        return total

    # Score all rows
    scored = []
    for i, row in enumerate(rows):
        scored.append((score_row(row), i))
    
    # Sort by score (ascending, as we want lower values for '-' and higher for '+')
    scored.sort(key=lambda x: x[0])
    
    # Return top 5% (or at least 1)
    limit = max(1, len(rows) // 20)
    return [item[1] for item in scored[:limit]]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
            
            best_indices = remember(header, rows)
            
            print("Customer Inquiry: Show me the past setups that turned out best.")
            print(f"Analysis: Identified {len(best_indices)} top-performing configurations.")
            print("These setups represent the top 5% of historical data based on goal optimization.")
            print(f"Example of a top-performing setup (Index {best_indices[0]}):")
            print(rows[best_indices[0]])
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
