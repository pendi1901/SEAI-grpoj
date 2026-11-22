import csv
from step01 import remember

def flow(header, row, seen):
    """
    Decides if the current row is a 'top performer' based on the 
    'YearsAtCompany+' goal, relative to the history seen so far.
    We use the logic from step01 to determine if this row belongs 
    in the top 5% of the current population.
    """
    # Combine current row with seen rows to evaluate relative standing
    all_rows = seen + [row]
    
    # Use the logic from step01 to identify indices of top performers
    # Note: remember() returns indices of the top 5%
    top_indices = remember(header, all_rows)
    
    # If the current row (the last one in all_rows) is in the top indices,
    # we flag it for a "what would keep you here" conversation.
    return (len(all_rows) - 1) in top_indices

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

    # Simulate the arrival process
    seen = []
    conversations_needed = 0
    for row in rows:
        if flow(header, row, seen):
            conversations_needed += 1
        seen.append(row)

    print(f"Processed {len(rows)} employees.")
    print(f"Total 'what would keep you here' conversations recommended: {conversations_needed}")
