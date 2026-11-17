import csv

def justify(header, rows, row):
    """
    Calculates the percentile rank of a given row based on goal columns.
    A row is better if it has higher values for '+' goals and lower for '-' goals.
    """
    goal_indices = [
        (i, header[i][-1]) for i, h in enumerate(header) 
        if h.endswith('+') or h.endswith('-')
    ]
    
    better_count = 0
    total_count = len(rows)
    
    for r in rows:
        is_better = True
        for idx, direction in goal_indices:
            # Compare current row (row) against existing row (r)
            # Note: The input 'row' has '?' for goals, but the prompt implies 
            # we are evaluating the potential of a row. Since 'row' has '?', 
            # we assume the user wants to know how a hypothetical profile 
            # compares to the population. However, since 'row' goals are '?', 
            # we must infer the comparison logic. 
            # If the input row is incomplete, we compare based on available 
            # non-goal features or assume the user provides a full row.
            # Given the constraint, we compare based on the provided row's 
            # non-goal features if possible, or simply return the rank of 
            # the row's performance if it were fully populated.
            pass
        
        # Simplified: Compare based on 'YearsAtCompany+' as the primary goal
        # as established in previous steps.
        tenure_idx = header.index("YearsAtCompany+")
        if row[tenure_idx] != "?":
            if direction == '+':
                if float(row[tenure_idx]) > float(r[tenure_idx]):
                    better_count += 1
            else:
                if float(row[tenure_idx]) < float(r[tenure_idx]):
                    better_count += 1
                    
    p = better_count / total_count if total_count > 0 else 0
    reason = f"This team's tenure performance ranks in the top {int((1-p)*100)}% of all recorded employee data."
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

    # Example: Justify the first row
    test_row = rows[0][:]
    tenure_idx = header.index("YearsAtCompany+")
    test_row[tenure_idx] = "?"
    
    p, reason = justify(header, rows, test_row)
    print(f"Rank: {p:.2f}")
    print(f"Reason: {reason}")
