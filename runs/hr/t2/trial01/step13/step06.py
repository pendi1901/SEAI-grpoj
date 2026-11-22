import csv
import step01

def get_score(header, row):
    """Calculates a score where higher is better."""
    score = 0
    for i, name in enumerate(header):
        if name.endswith('+'):
            score += row[i]
        elif name.endswith('-'):
            score -= row[i]
    return score

def justify(header, rows, row):
    """
    Estimates the score of the target row by averaging the scores of rows
    with matching symbolic input values, then compares it to all rows.
    """
    # Identify input columns (non-goal, non-numeric)
    symbolic_indices = [i for i, name in enumerate(header) 
                        if not name.endswith('+') and not name.endswith('-') 
                        and not header[i][0].isupper()]
    
    # Find rows that match the symbolic inputs of the target row
    matches = []
    for r in rows:
        if all(r[i] == row[i] for i in symbolic_indices):
            matches.append(get_score(header, r))
    
    # Estimate score: use average of matches, or global average if no matches
    if matches:
        est_score = sum(matches) / len(matches)
    else:
        all_scores = [get_score(header, r) for r in rows]
        est_score = sum(all_scores) / len(all_scores)
    
    # Compare estimated score against all rows
    all_scores = [get_score(header, r) for r in rows]
    better_than = [s for s in all_scores if est_score > s]
    p = len(better_than) / len(all_scores)
    
    reason = f"This arrangement ranks in the top {int((1-p)*100)}% of all teams because its estimated tenure score of {est_score:.1f} outperforms {int(p*100)}% of the historical records."
    
    return p, reason

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)
    
    # Test with the first row, masking its goal columns
    test_row = list(rows[0])
    for i, name in enumerate(header):
        if name.endswith('+') or name.endswith('-'):
            test_row[i] = "?"
            
    p, reason = justify(header, rows, test_row)
    print(reason)
