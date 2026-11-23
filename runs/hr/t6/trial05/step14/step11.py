import ezr
import random

def remember(header, rows):
    """
    Finds the people most like the first row in the dataset and reports 
    their tenure (YearsAtCompany+).
    """
    # Create a table object to use distance metrics
    tbl = ezr.Tbl([header] + rows)
    
    # The target is the first row
    target = rows[0]
    
    # Calculate distance from the target for all rows (excluding the target itself)
    # We use xdist to find rows most similar in input space
    scored = []
    for i, row in enumerate(rows):
        if i == 0: continue
        d = ezr.xdist(tbl, row, target)
        scored.append((d, i))
    
    # Sort by distance (ascending, so most similar first)
    scored.sort(key=lambda x: x[0])
    
    # Return the top 5% of rows (800 rows * 0.05 = 40)
    limit = max(1, int(len(rows) * 0.05))
    return [item[1] for item in scored[:limit]]

if __name__ == "__main__":
    # Load data
    data = list(ezr.csv("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"))
    header = data[0]
    rows = data[1:]
    
    # Get indices of similar rows
    similar_indices = remember(header, rows)
    
    # Map indices to names for readability
    col_map = {name: i for i, name in enumerate(header)}
    tenure_idx = col_map['YearsAtCompany+']
    
    # Calculate average tenure of these similar people
    tenures = [rows[i][tenure_idx] for i in similar_indices]
    avg_tenure = sum(tenures) / len(tenures)
    
    print(f"Identified {len(similar_indices)} employees most similar to the first record.")
    print(f"Average tenure (YearsAtCompany+) for this similar group: {avg_tenure:.2f} years.")
    print("These individuals were selected based on minimal input-space distance.")
    
    exit(0)
