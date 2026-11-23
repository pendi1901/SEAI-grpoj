import csv
import step03

def flow(header, row, seen):
    """
    Detects if a new row is an outlier compared to the 'seen' population.
    We use the statistical similarity check from step03 on the sum of 
    goal columns to determine if the new row represents a shift in 
    the team's performance distribution.
    """
    if not seen:
        return False
    
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    def get_score(r):
        score = 0
        for i in goal_indices:
            val = r[i]
            if isinstance(val, (int, float)):
                if header[i].endswith('+'):
                    score += val
                else:
                    score -= val
        return score

    # Get scores of seen population
    seen_scores = [get_score(r) for r in seen]
    
    # If the new row's score is statistically different from the seen population,
    # it indicates the team no longer looks the way it normally does.
    # We use the certify logic: if certify returns False, they are different.
    is_similar = step03.certify(seen_scores, [get_score(row)])
    
    return not is_similar

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
            
    seen = []
    anomalies = 0
    for row in rows:
        if flow(header, row, seen):
            anomalies += 1
        seen.append(row)
        
    print("Team Stability Analysis:")
    print(f"Processed {len(rows)} monthly survey records.")
    print(f"Detected {anomalies} instances where the team's performance profile shifted significantly.")
    print("When this count is high, the team no longer looks like its historical norm.")
