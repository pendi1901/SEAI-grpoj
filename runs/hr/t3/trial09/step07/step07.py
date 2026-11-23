import csv
import random

def choose(header, rows, label):
    """
    Finds the best row by sampling 50 rows, labeling them to get their 
    true goal values, and returning the index of the row with the 
    highest value in the first goal column ('YearsAtCompany+').
    """
    # Identify the goal column (first one ending in + or -)
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-'))
    
    # We have a budget of 50 labels.
    # We will sample 50 random indices from the available rows.
    num_rows = len(rows)
    sample_size = min(50, num_rows)
    indices_to_sample = random.sample(range(num_rows), sample_size)
    
    best_idx = -1
    best_val = -float('inf')
    
    for i in indices_to_sample:
        # label(i) returns a list of true goal values for that row
        goals = label(i)
        val = goals[0] # We focus on the first goal column
        
        if val > best_val:
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
            
    # Identify goal column index for the label function
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-'))
    
    # Define the label function for the harness
    def label(i):
        return [rows[i][goal_idx]]
    
    # Run the selection
    best_index = choose(header, rows, label)
    
    print("Analysis Complete.")
    print(f"The best row found within the 50-interview budget is index {best_index}.")
    print(f"YearsAtCompany+ for this employee: {rows[best_index][goal_idx]}")
    print("This employee represents the longest-staying arrangement found in our sample.")
