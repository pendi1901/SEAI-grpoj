import csv
import step01

def flow(header, row, seen):
    """
    Detects if a team no longer looks like it normally does.
    We compare the current row's numeric values to the distribution of 
    the 'seen' rows. If the current row is an outlier (more than 2 
    standard deviations from the mean of seen rows) in any goal column, 
    we flag it as a change in team composition.
    """
    if not seen:
        return False

    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    
    for idx in goal_indices:
        vals = [r[idx] for r in seen if isinstance(r[idx], (int, float))]
        if len(vals) < 5:
            continue
            
        mean = sum(vals) / len(vals)
        var = sum((x - mean) ** 2 for x in vals) / len(vals)
        std = var ** 0.5
        
        if std == 0:
            continue
            
        # If the new row is significantly different (2 std devs) from the norm
        if abs(row[idx] - mean) > (2 * std):
            return True
            
    return False

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    header = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            new_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    try:
                        new_row.append(float(val))
                    except ValueError:
                        new_row.append(0.0)
                else:
                    new_row.append(val)
            rows.append(new_row)
            
    seen = []
    anomalies = 0
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            anomalies += 1
        seen.append(row)
        
    print(f"Analysis complete: Detected {anomalies} instances where the team composition "
          "deviated significantly from historical norms.")
    print("A team no longer looks 'normal' when new arrivals show tenure metrics "
          "that are statistical outliers compared to the existing team.")
