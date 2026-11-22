import csv

def justify(header, rows, row):
    """
    Ranks the provided row against the dataset based on tenure goals.
    A row is 'better' if its sum of tenure-related metrics is higher.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+')]
    
    def get_score(r):
        # Sum the goal columns. If goal is '?', we estimate it as the global mean.
        score = 0
        for i in goal_indices:
            val = r[i]
            if val == "?":
                # Calculate mean of this column from known rows
                known = [float(x[i]) for x in rows if x[i] != "?"]
                val = sum(known) / len(known) if known else 0
            score += float(val)
        return score

    target_score = get_score(row)
    
    # Compare against all rows
    better_count = 0
    for r in rows:
        if get_score(r) < target_score:
            better_count += 1
            
    p = better_count / len(rows)
    reason = f"This arrangement ranks better than {p:.1%} of the existing staff records based on combined tenure metrics."
    
    return p, reason

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    header = []
    
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
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    # Test with the last row as a sample
    test_row = list(rows[-1])
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+')]
    for idx in goal_indices:
        test_row[idx] = "?"
        
    p, reason = justify(header, rows, test_row)
    print(f"Rank: {p:.4f}")
    print(f"Reason: {reason}")
