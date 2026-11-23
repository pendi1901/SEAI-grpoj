import csv
from step01 import remember

def flow(header, row, seen):
    """
    Decides if the current row is an employee who should have a 
    'what would keep you here' conversation.
    
    Strategy: We define 'unusually long' tenure as the top 5% of 
    the population. If the current row's tenure ('YearsAtCompany+') 
    is in the top 5% of the historical data (seen + current), 
    we flag them for a conversation.
    """
    tenure_idx = header.index('YearsAtCompany+')
    current_tenure = row[tenure_idx]
    
    # Combine seen rows with current row to evaluate relative standing
    all_rows = seen + [row]
    
    # Use the logic from step01 to identify the threshold for the top 5%
    # We pass the current set of rows to determine if the current row is 'best'
    best_indices = remember(header, all_rows)
    
    # If the current row is among the identified 'best' (unusually long tenure),
    # we trigger the conversation.
    return (len(all_rows) - 1) in best_indices

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
    conversations_needed = 0
    for row in rows:
        if flow(header, row, seen):
            conversations_needed += 1
        seen.append(row)

    print(f"Analysis complete.")
    print(f"Total employees processed: {len(rows)}")
    print(f"Number of employees identified for a 'what would keep you here' conversation: {conversations_needed}")
    print("These employees represent the top 5% of tenure at the company.")
