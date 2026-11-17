import csv

def justify(header, rows, row):
    """
    Ranks a row's performance against historical data based on goal columns.
    A row is 'better' if its goal values are higher for '+' columns 
    and lower for '-' columns.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    
    better_count = 0
    total_rows = len(rows)
    
    for r in rows:
        is_better = True
        for idx in goal_indices:
            col_name = header[idx]
            val_r = r[idx]
            val_row = row[idx]
            
            # Skip if the row being tested has unknown goal values
            if val_row == "?":
                is_better = False
                break
            
            if col_name.endswith('+'):
                if not (val_row >= val_r):
                    is_better = False
                    break
            elif col_name.endswith('-'):
                if not (val_row <= val_r):
                    is_better = False
                    break
        
        if is_better:
            better_count += 1
            
    p = better_count / total_rows if total_rows > 0 else 0
    reason = f"This team's arrangement outperforms {p:.1%} of historical records based on tenure and retention goals."
    
    return (p, reason)

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.train.csv"
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # Example: Test the first row as if it were a new query
    test_row = list(rows[0])
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    for idx in goal_indices:
        test_row[idx] = "?"
        
    p, reason = justify(header, rows, test_row)
    print(f"Rank: {p:.4f}")
    print(f"Reason: {reason}")
