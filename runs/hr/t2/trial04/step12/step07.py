import csv
import step01
import step02

def choose(header, rows, label):
    """
    Finds the best working arrangement by sampling 50 rows.
    We use a simple strategy: sample 50 rows, label them, 
    and pick the one with the highest 'YearsAtCompany+'.
    """
    # Identify goal column
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-'))
    
    # We can label at most 50 rows. 
    # We pick 50 indices spread across the dataset.
    n = len(rows)
    sample_indices = [int(i * (n / 50)) for i in range(50)]
    
    best_idx = -1
    best_val = -float('inf')
    
    for i in sample_indices:
        # label(i) returns a list of true goal values for row i
        # The prompt implies the goal column is the one we are interested in.
        true_goals = label(i)
        val = true_goals[0] # Assuming the first goal is the one to maximize
        
        if val > best_val:
            best_val = val
            best_idx = i
            
    return best_idx

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

    # Prepare the label function for the harness
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-'))
    
    labeled_data = {}
    def label(i):
        if i not in labeled_data:
            labeled_data[i] = [rows[i][goal_idx]]
        return labeled_data[i]

    best_row_idx = choose(header, rows, label)
    
    print(f"Analysis complete. Best row found at index {best_row_idx}.")
    print(f"Value for 'YearsAtCompany+': {rows[best_row_idx][goal_idx]}")
