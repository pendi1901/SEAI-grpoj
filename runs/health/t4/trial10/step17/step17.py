import csv
import random
from step01 import remember
from step02 import guess

def choose(header, rows, label):
    """
    Finds a setup that forecasts well (using a model) and is small (using N_estimators).
    We sample 50 rows, label them, and rank them based on a combination of
    predicted performance and small size.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    size_idx = header.index('N_estimators')
    
    # 1. Sample 50 rows
    indices = list(range(len(rows)))
    sample_indices = random.sample(indices, min(50, len(rows)))
    
    # 2. Label the sampled rows
    labeled_data = []
    for idx in sample_indices:
        true_goals = label(idx)
        row_copy = list(rows[idx])
        for i, g_idx in enumerate(goal_indices):
            row_copy[g_idx] = true_goals[i]
        labeled_data.append((idx, row_copy))
    
    # 3. Rank based on multi-objective: 
    # We want to minimize goals ending in '-', maximize goals ending in '+',
    # and minimize N_estimators (small size).
    # We create a temporary header/rows for the remember function.
    temp_header = list(header)
    temp_header[size_idx] = "N_estimators-" # Treat size as a goal to minimize
    
    temp_rows = []
    for idx, row in labeled_data:
        temp_rows.append(row)
        
    best_local_indices = remember(temp_header, temp_rows)
    
    # Return the original index of the best row found
    return labeled_data[best_local_indices[0]][0]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    header = []
    
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                processed_row = []
                for val in row:
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)
        
        def label(i):
            return [rows[i][j] for j, name in enumerate(header) if name.endswith(('-', '+'))]
        
        masked_rows = []
        for r in rows:
            new_row = list(r)
            for j, name in enumerate(header):
                if name.endswith(('-', '+')):
                    new_row[j] = '?'
            masked_rows.append(new_row)
            
        best_idx = choose(header, masked_rows, label)
        print(f"The best setup that balances performance and small size is at index: {best_idx}")
        exit(0)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
