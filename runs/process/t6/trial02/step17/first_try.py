import ezr
import step07

def choose(header, rows, label):
    """
    Find the best setup for a large, high-criticality project.
    We filter for high 'Size' and 'Criticality' to focus on the 
    customer's specific project profile, then use the acquisition 
    logic from step07 to find the best configuration within the budget.
    """
    # 1. Filter for large, critical projects
    # 'Size' is index 6, 'Criticality' is index 1
    size_idx = 6
    crit_idx = 1
    
    # Define "large" and "critical" as above the median
    sizes = [r[size_idx] for r in rows]
    crits = [r[crit_idx] for r in rows]
    med_size = sorted(sizes)[len(sizes) // 2]
    med_crit = sorted(crits)[len(crits) // 2]
    
    # Prioritize rows that match the profile
    def score_profile(row):
        return (row[size_idx] >= med_size) + (row[crit_idx] >= med_crit)
    
    # Sort rows by profile match (descending)
    indexed_rows = list(enumerate(rows))
    indexed_rows.sort(key=lambda x: score_profile(x[1]), reverse=True)
    
    # We use the first 200 candidates that match the profile
    candidates = [x[0] for x in indexed_rows[:200]]
    
    # 2. Use the acquisition logic to find the best within the budget
    # We pass a subset of rows to the choose function logic
    # We need to adapt the label function to map indices correctly
    def oracle_wrapper(idx):
        return label(idx)
    
    # We use the logic from step07, but restricted to our candidates
    # to ensure we don't waste labels on irrelevant project types.
    # We create a temporary list of rows for the choose function
    subset_rows = [rows[i] for i in candidates]
    
    # We need to map the internal index back to the original index
    def subset_label(i):
        return oracle_wrapper(candidates[i])
    
    best_in_subset = step07.choose(header, subset_rows, subset_label)
    
    return candidates[best_in_subset]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        all_rows = list(data_gen)
    except StopIteration:
        exit(1)
        
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    masked_rows = []
    for row in all_rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    def label_func(idx):
        return all_rows[idx]
        
    best_idx = choose(header, masked_rows, label_func)
    
    print(f"Optimization complete for large, high-criticality project.")
    print(f"Best row found at index: {best_idx}")
    print(f"Goal values for best row: {[all_rows[best_idx][i] for i in goal_indices]}")
    
    exit(0)
