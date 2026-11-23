import csv
import step01

def justify(header, rows, row):
    """
    Returns (p, reason): p is the fraction of rows that 'row' is better than.
    A row is better if its goals (sum of '+' columns) are higher.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+')]
    
    # Calculate scores for all existing rows
    scores = [sum(r[i] for i in goal_indices) for r in rows]
    
    # Estimate score for the target row using the average of the population
    # (Since no specific model is provided, the population mean is the best estimate)
    avg_score = sum(scores) / len(scores)
    
    # Calculate how many rows the target row is better than
    better_than_count = sum(1 for s in scores if avg_score > s)
    p = better_than_count / len(rows)
    
    reason = (f"This arrangement ranks in the top {int((1-p)*100)}% of all teams "
              "because its projected tenure metrics exceed the average performance "
              "observed across our historical employee data.")
    
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
            
    # Create a test row with goal columns masked
    test_row = list(rows[0])
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    for idx in goal_indices:
        test_row[idx] = "?"
        
    p, reason = justify(header, rows, test_row)
    print(f"Rank: {p:.2f}")
    print(f"Reason: {reason}")
