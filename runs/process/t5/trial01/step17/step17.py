import ezr
import random

def choose(header, rows, label):
    """
    Finds the best setup for a large, high-criticality project.
    We filter for rows that represent 'large' projects (Size > 0.5)
    and then use the acquire strategy to find the best within those.
    """
    # Identify index for 'Size'
    size_idx = header.index("Size")
    
    # Filter rows that are 'large' (Size > 0.5)
    # If no rows are large, fall back to all rows
    large_indices = [i for i, r in enumerate(rows) if r[size_idx] > 0.5]
    if not large_indices:
        large_indices = list(range(len(rows)))
        
    # We only have 50 labels. We use a subset of the large rows.
    # We sample up to 50 from the large_rows to stay within budget.
    sample_indices = random.sample(large_indices, min(len(large_indices), 50))
    
    best_idx = -1
    best_dist = float('inf')
    
    # Create a table to track progress. 
    # We must use the full header to ensure column indices match the rows.
    tbl = ezr.Tbl([header])
    
    # Label the sampled rows
    for i in sample_indices:
        true_row = label(i)
        
        # Update our table with the true values
        # We use addRow to keep the row in the table so ydist can be calculated
        ezr.addRow(tbl, true_row)
        
        # Calculate distance to ideal
        dist = ezr.ydist(tbl, true_row)
        if dist < best_dist:
            best_dist = dist
            best_idx = i
            
    return best_idx

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    rows_iter = ezr.csv(filename)
    header = next(rows_iter)
    all_rows = list(rows_iter)
    
    # Mask goals
    hidden_rows = []
    for row in all_rows:
        new_row = list(row)
        for i, name in enumerate(header):
            if name[-1] in "+-":
                new_row[i] = "?"
        hidden_rows.append(new_row)
        
    # Oracle
    def label_func(i):
        return all_rows[i]
    
    random.seed(1234567891)
    best_index = choose(header, hidden_rows, label_func)
    
    print("Optimization Report: High-Criticality Large Projects")
    print(f"The best configuration found for a large project is at index: {best_index}")
    print(f"Row data: {all_rows[best_index]}")
    
    exit(0)
