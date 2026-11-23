import csv

def flow(header, row, seen):
    """
    Detects if a team's composition has shifted significantly.
    We compare the current row's numeric profile (mean of all numeric inputs)
    against the distribution of the 'seen' rows. If the current row is 
    an outlier (e.g., beyond 2 standard deviations from the mean of seen rows),
    we flag it as a shift in team composition.
    """
    if len(seen) < 30:
        return False

    # Identify numeric input columns (excluding goals)
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    numeric_indices = [i for i, name in enumerate(header) if name[0].isupper() and i not in goal_indices]
    
    def get_numeric_features(r):
        return [float(r[i]) for i in numeric_indices if isinstance(r[i], (int, float))]

    current_features = get_numeric_features(row)
    if not current_features:
        return False

    # Calculate mean and std of the 'seen' data for the first numeric feature (Age)
    # as a proxy for team demographic shift
    age_idx = header.index('Age')
    seen_ages = [r[age_idx] for r in seen if isinstance(r[age_idx], (int, float))]
    
    if len(seen_ages) < 30:
        return False
        
    mean_age = sum(seen_ages) / len(seen_ages)
    std_age = (sum((x - mean_age) ** 2 for x in seen_ages) / len(seen_ages)) ** 0.5
    
    # If the current employee's age is more than 2 standard deviations away,
    # we flag this as a potential shift in team composition.
    if std_age > 0 and abs(row[age_idx] - mean_age) > (2 * std_age):
        return True
        
    return False

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
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    seen = []
    shifts = 0
    for row in rows:
        if flow(header, row, seen):
            shifts += 1
        seen.append(row)
    
    print(f"Analysis complete: Detected {shifts} instances where the team composition "
          "shifted significantly based on age demographics.")
    print("Logic: Flagged rows where the employee's age is an outlier (> 2 standard deviations) "
          "relative to the previously observed team members.")
