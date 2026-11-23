import csv
from step01 import remember

def flow(header, row, seen):
    """
    Decides if the current row is a candidate for a 'retention conversation'.
    We compare the current row's 'YearsAtCompany+' against the distribution 
    of 'seen' rows. If the current row is in the top 5% of the combined 
    history (or if it's the first row), we flag it.
    """
    goal_idx = header.index('YearsAtCompany+')
    
    # If no history, we can't compare, so we take the first one
    if not seen:
        return True
    
    # Combine current row with history to determine the threshold
    all_rows = seen + [row]
    years = [r[goal_idx] for r in all_rows]
    
    # Calculate threshold for top 5%
    sorted_years = sorted(years, reverse=True)
    limit = max(1, len(all_rows) // 20)
    threshold = sorted_years[limit - 1]
    
    # If this row meets or exceeds the threshold, flag it
    return row[goal_idx] >= threshold

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed_row)
    
    seen = []
    selected_count = 0
    for row in rows:
        if flow(header, row, seen):
            selected_count += 1
        seen.append(row)
    
    print(f"Processed {len(rows)} employees.")
    print(f"Retention conversations recommended for: {selected_count} employees.")
    print("Logic: Flagged employees who are in the top 5% of 'YearsAtCompany+' based on arrival history.")
