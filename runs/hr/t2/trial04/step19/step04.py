import csv
import step01
import step03

def flow(header, row, seen):
    """
    Decides if the current employee needs a 'what would keep you here' 
    conversation. We target those with low 'YearsAtCompany+' compared 
    to the average of those seen so far, or those who are outliers.
    """
    yac_idx = header.index("YearsAtCompany+")
    
    # If this is the first row, we can't compare, so let it go
    if not seen:
        return False
    
    # Calculate the mean of 'YearsAtCompany+' for all seen rows
    seen_vals = [r[yac_idx] for r in seen if isinstance(r[yac_idx], (int, float))]
    if not seen_vals:
        return False
    
    mean_yac = sum(seen_vals) / len(seen_vals)
    current_yac = row[yac_idx]
    
    # If the current employee has significantly lower tenure than the average
    # of those seen, they are a candidate for a retention conversation.
    # Using a simple threshold: if they are in the bottom 25% of the mean.
    if current_yac < (mean_yac * 0.75):
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

    # Simulate the flow
    seen = []
    selected_count = 0
    for row in rows:
        if flow(header, row, seen):
            selected_count += 1
        seen.append(row)
    
    print(f"Analysis complete. Processed {len(rows)} employees.")
    print(f"Identified {selected_count} employees for 'what would keep you here' conversations.")
