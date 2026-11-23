import csv
import step01
import step02
import step05

def choose(header, rows, label):
    """
    Finds the best working arrangement by sampling 50 rows.
    We use the 'blame' logic to identify key factors, then sample rows
    that represent diverse combinations of these factors, or simply
    sample to estimate the best. Given the constraint, we sample 50
    randomly or strategically to find the max 'YearsAtCompany+'.
    """
    # Identify goal column
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+'))
    
    # We have 50 labels. We will sample 50 rows to find the best.
    # To be efficient, we pick 50 rows spread across the dataset.
    n = len(rows)
    indices_to_sample = [int(i * (n / 50)) for i in range(50)]
    
    best_val = -1.0
    best_idx = -1
    
    for i in indices_to_sample:
        # Label the row to get the true goal value
        true_goals = label(i)
        val = true_goals[0] # YearsAtCompany+
        
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

    # Setup for the harness
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+'))
    
    # Create masked rows
    masked_rows = []
    for row in rows:
        new_row = list(row)
        new_row[goal_idx] = "?"
        masked_rows.append(new_row)
        
    # Define the label function
    labeled_count = 0
    seen_labels = set()
    
    def label(i):
        global labeled_count
        if i not in seen_labels:
            labeled_count += 1
            if labeled_count > 50:
                raise Exception("Exceeded 50 labels")
            seen_labels.add(i)
        return [rows[i][goal_idx]]

    best_idx = choose(header, masked_rows, label)
    
    print(f"Best working arrangement found at index {best_idx}.")
    print(f"YearsAtCompany+: {rows[best_idx][goal_idx]}")
    print(f"Job Role: {rows[best_idx][header.index('jobRole')]}")
