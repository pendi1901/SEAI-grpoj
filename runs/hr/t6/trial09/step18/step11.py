import ezr
import random

def remember(header, rows):
    """
    Finds the 5% of rows that are most similar to the 'best' performing 
    employees in the dataset.
    """
    # Create a table to use ezr's distance functions
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for all rows to identify the 'best' performers
    # Lower ydist is better.
    scored = []
    for i, row in enumerate(rows):
        scored.append((ezr.ydist(tbl, row), i))
    
    # Sort by ydist ascending (best first)
    scored.sort()
    
    # We want to return 5% of the rows (800 * 0.05 = 40)
    limit = max(1, int(len(rows) * 0.05))
    
    # Return the indices of the top 5%
    return [idx for score, idx in scored[:limit]]

def find_similar(header, rows, target_row, n=5):
    """
    Finds the N rows most similar to target_row based on x-columns.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate x-distance to the target row
    distances = []
    for i, row in enumerate(rows):
        d = ezr.xdist(tbl, target_row, row)
        distances.append((d, i))
    
    # Sort by distance ascending (most similar first)
    distances.sort()
    
    # Return indices of the top N similar rows
    return [idx for d, idx in distances[:n]]

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # 1. Identify the best employees (as per the remember function requirement)
    best_indices = remember(header, rows)
    
    # 2. Pick a random employee to compare against
    target_idx = random.choice(range(len(rows)))
    target_row = rows[target_idx]
    
    # 3. Find the most similar people
    similar_indices = find_similar(header, rows, target_row, n=5)
    
    # 4. Report findings
    print(f"Analysis for employee at index {target_idx}:")
    print("The following employees are most similar in profile:")
    
    # YearsAtCompany+ is at index 31
    yac_idx = 31
    for idx in similar_indices:
        stayed = rows[idx][yac_idx]
        print(f" - Employee {idx}: Stayed {stayed} years.")
        
    print(f"\nNote: The 'best' performing employees (top 5%) were identified at indices: {best_indices[:5]}...")
    exit(0)
