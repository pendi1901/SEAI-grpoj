import csv
import step01

def flow(header, row, seen):
    """
    Decides if the current row is a 'top performer' based on tenure metrics.
    We use the logic from step01 to determine if the current row is in the 
    top 5% of the cumulative data seen so far.
    """
    # Identify goal indices
    goals = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    # Calculate score for current row
    # For +, higher is better. For -, lower is better.
    # Since step01 focused on +, we adapt:
    def get_score(r):
        score = 0
        for i in goals:
            val = r[i]
            if header[i].endswith('+'):
                score += val
            else:
                score -= val
        return score

    current_score = get_score(row)
    
    # Compare against all previously seen rows
    # If this row is better than at least 95% of seen rows, we flag it.
    if not seen:
        return True
    
    seen_scores = [get_score(r) for r in seen]
    better_than = sum(1 for s in seen_scores if current_score > s)
    
    # If it's in the top 5% of what we've seen so far
    return better_than >= (len(seen_scores) * 0.95)

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

    seen = []
    flagged_count = 0
    for row in rows:
        if flow(header, row, seen):
            flagged_count += 1
        seen.append(row)

    print(f"Analysis complete.")
    print(f"Total employees processed: {len(rows)}")
    print(f"Employees identified for 'what would keep you here' conversation: {flagged_count}")
    print("Decision logic: Flagged if employee tenure metrics are in the top 5% of history.")
