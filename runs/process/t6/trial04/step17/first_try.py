import ezr
import step07

def choose(header, rows, label):
    """
    Find the best setup for a large, high-stakes project.
    Since failure is damaging, we prioritize finding a robust, 
    high-performing configuration using the acquire strategy.
    """
    # The customer specifies the project is "large".
    # We filter the rows to focus on those with high 'Size' values.
    size_idx = header.index("Size")
    
    # Identify the median size to define "large"
    sizes = [r[size_idx] for r in rows]
    median_size = sorted(sizes)[len(sizes) // 2]
    
    # Filter rows to only consider large projects
    large_indices = [i for i, r in enumerate(rows) if r[size_idx] >= median_size]
    large_rows = [rows[i] for i in large_indices]
    
    # Map back to original indices for the label function
    def oracle_wrapper(row):
        for i, r in enumerate(rows):
            if r is row:
                return label(i)
        return row

    # Use the acquire strategy on the large project subset
    # We limit the budget to 50 as per the requirement
    ezr.the.Stop = 50
    tbl = ezr.Tbl([header] + large_rows)
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Find the best row among those labeled
    labeled_tbl = ezr.Tbl([header] + labeled_rows)
    best_row = min(labeled_tbl.rows, key=lambda r: ezr.ydist(labeled_tbl, r))
    
    # Return the original index of the best row found
    for i, r in enumerate(rows):
        if r is best_row:
            return i
    return large_indices[0]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    rows_gen = ezr.csv(filename)
    header = next(rows_gen)
    rows = list(rows_gen)
    
    # Mask the goals
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
    
    def label(i):
        return rows[i]
    
    best_idx = choose(header, masked_rows, label)
    
    print("Optimization for Large-Scale High-Stakes Projects:")
    print("-" * 60)
    print(f"Best configuration found at index: {best_idx}")
    goal_vals = [rows[best_idx][i] for i in goal_indices]
    print(f"Goal values: {goal_vals}")
    print("-" * 60)
    print("Strategy: Filtered for large-scale projects and applied intelligent")
    print("sampling to minimize risk and maximize performance.")
