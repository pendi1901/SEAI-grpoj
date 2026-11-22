import ezr
import step01
import step09

def remember(header, rows):
    """
    Find the rows most similar to the 'best' rows found in the dataset.
    We define 'best' as the top 5% by ydist, then find the rows 
    closest to those in the input (X) space.
    """
    # Use step01 to identify the indices of the top 5% of rows
    best_indices = step01.remember(header, rows)
    best_rows = [rows[i] for i in best_indices]
    
    # Create a table to facilitate distance calculations
    tbl = ezr.Tbl([header] + rows)
    
    # For every row in the dataset, find its distance to the nearest 'best' row
    # We want to return rows that are 'most like' the best ones
    similarities = []
    for i, row in enumerate(rows):
        # Distance to the closest best row
        d = min(ezr.xdist(tbl, row, best_row) for best_row in best_rows)
        similarities.append((d, i))
    
    # Sort by distance ascending (closest to best rows first)
    similarities.sort(key=lambda x: x[0])
    
    # Return the top 5% of rows that are most similar to the best ones
    limit = max(1, int(len(rows) * 0.05))
    return [item[1] for item in similarities[:limit]]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
    except StopIteration:
        exit(1)
        
    # Get the indices of rows most similar to the best performers
    similar_indices = remember(header, rows)
    
    print("Analysis: Finding past setups most similar to our best performers.")
    print(f"Found {len(similar_indices)} highly similar configurations.")
    print("-" * 60)
    print(f"{'Index':<10} | {'Cost-':<10} | {'Score-':<10} | {'Idle-':<10}")
    print("-" * 60)
    
    goal_cols = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    
    for idx in similar_indices:
        row = rows[idx]
        goals = [f"{row[i]:.4f}" for i in goal_cols]
        print(f"{idx:<10} | {goals[0]:<10} | {goals[1]:<10} | {goals[2]:<10}")
        
    exit(0)
