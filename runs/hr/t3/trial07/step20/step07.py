import csv
import random

def choose(header, rows, label):
    """
    Finds the working arrangement that keeps people longest by sampling 50 rows.
    The label(i) function returns the full row (including goals) for index i.
    """
    # Identify goal column index
    goal_idx = -1
    for i, name in enumerate(header):
        if name.endswith('+') or name.endswith('-'):
            goal_idx = i
            break
            
    # Select 50 random indices to sample
    num_samples = min(50, len(rows))
    indices = random.sample(range(len(rows)), num_samples)
    
    best_val = -float('inf')
    best_idx = -1
    
    # Determine if we are maximizing (+) or minimizing (-)
    is_maximize = header[goal_idx].endswith('+')
    
    for i in indices:
        # Query the true row data
        full_row = label(i)
        val = full_row[goal_idx]
        
        # Update best based on goal type
        if is_maximize:
            if val > best_val:
                best_val = val
                best_idx = i
        else:
            if val < best_val or best_idx == -1:
                best_val = val
                best_idx = i
            
    return best_idx

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
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    # Create a copy of rows with goals masked for the choose function
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-'))
    masked_rows = []
    for row in rows:
        new_row = list(row)
        new_row[goal_idx] = "?"
        masked_rows.append(new_row)
        
    # Define the label function for the harness
    def label(i):
        return rows[i]
        
    best_idx = choose(header, masked_rows, label)
    
    print(f"Analysis complete.")
    print(f"The best working arrangement found is at row index: {best_idx}")
    print(f"Goal value ({header[goal_idx]}): {rows[best_idx][goal_idx]}")
    print("Strategy: Sampled 50 random employees to identify the best working arrangement.")
