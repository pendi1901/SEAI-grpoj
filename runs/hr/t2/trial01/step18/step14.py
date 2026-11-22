import csv
import step06

def flow(header, row, seen):
    """
    Detects if a team's composition has shifted significantly.
    We compare the current row's tenure score to the distribution of 
    tenure scores in the 'seen' history. If the current row is an 
    outlier (e.g., > 2 standard deviations from the mean of seen rows),
    we flag it as a shift in team composition.
    """
    if len(seen) < 30:
        return False
    
    # Calculate scores for all seen rows
    seen_scores = [step06.get_score(header, r) for r in seen]
    
    # Calculate mean and standard deviation of seen scores
    mean = sum(seen_scores) / len(seen_scores)
    variance = sum((s - mean) ** 2 for s in seen_scores) / len(seen_scores)
    std = variance ** 0.5
    
    # Current row score
    current_score = step06.get_score(header, row)
    
    # If std is 0, we can't detect a shift
    if std == 0:
        return False
    
    # Flag if the current row is more than 2 standard deviations away
    z_score = abs(current_score - mean) / std
    return z_score > 2.0

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
    shifts = 0
    for row in rows:
        if flow(header, row, seen):
            shifts += 1
        seen.append(row)
    
    print("Team Composition Analysis:")
    print(f"Total records processed: {len(rows)}")
    print(f"Significant shifts detected: {shifts}")
    print("Logic: A shift is flagged when a new employee's tenure score deviates")
    print("by more than 2 standard deviations from the historical team average.")
