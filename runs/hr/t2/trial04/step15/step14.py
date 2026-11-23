import csv
import step03

def flow(header, row, seen):
    """
    Detects if a team's composition has drifted significantly.
    We compare the distribution of numeric inputs of the current row
    against the historical distribution of 'seen' rows using a 
    statistical similarity check (T-test).
    """
    if len(seen) < 30:
        return False

    # Identify numeric input columns
    numeric_indices = [i for i, name in enumerate(header) 
                       if name[0].isupper() and not (name.endswith('+') or name.endswith('-'))]
    
    # We check if the current row's numeric profile is an outlier 
    # compared to the 'seen' population.
    # We use the average of numeric columns as a proxy for the 'team state'.
    def get_profile(r):
        vals = [r[i] for i in numeric_indices if isinstance(r[i], (int, float))]
        return sum(vals) / len(vals) if vals else 0

    seen_profiles = [get_profile(r) for r in seen]
    current_profile = get_profile(row)
    
    # If the current profile is statistically different from the seen history,
    # we flag it as a shift in team composition.
    # We use step03.certify to check if the current row belongs to the same distribution.
    # Since certify takes two lists, we compare the current row (as a list) 
    # against the history.
    return not step03.certify([current_profile], seen_profiles)

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
    drift_count = 0
    for row in rows:
        if flow(header, row, seen):
            drift_count += 1
        seen.append(row)
    
    print(f"Analysis complete: Detected {drift_count} instances where the team composition shifted significantly.")
