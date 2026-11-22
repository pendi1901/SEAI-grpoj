import csv
from step01 import remember

def flow(header, row, seen):
    """
    Decides if the current row is 'unusually long' (top 5% of all time)
    based on the history of rows seen so far.
    """
    yac_idx = header.index('YearsAtCompany+')
    
    # If this is the first row, we can't compare, so let it go
    if not seen:
        return False
    
    # Combine current row with seen rows to determine the threshold
    all_rows = seen + [row]
    
    # Use the logic from step01 to find the top 5% threshold
    years = [r[yac_idx] for r in all_rows]
    sorted_years = sorted(years, reverse=True)
    limit = max(1, len(all_rows) // 20)
    threshold = sorted_years[limit - 1]
    
    # If the current row meets or exceeds the threshold, flag it
    return row[yac_idx] >= threshold

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
    
    # Simulate the arrival of rows one by one
    seen = []
    flagged_count = 0
    for row in rows:
        if flow(header, row, seen):
            flagged_count += 1
        seen.append(row)
    
    print(f"Analysis complete.")
    print(f"Total employees processed: {len(rows)}")
    print(f"Employees identified for 'what would keep you here' conversation: {flagged_count}")
    print("Decision logic: Flagged employees in the top 5% of 'YearsAtCompany+' relative to history.")
