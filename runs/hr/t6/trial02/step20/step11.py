import ezr
import random

def find_similar(header, rows, target_row, k=5):
    """
    Finds the k rows most similar to target_row in the x-space.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate distance from target_row to all other rows
    distances = []
    for i, row in enumerate(rows):
        # Skip if it's the target row itself (if present in rows)
        if row == target_row:
            continue
        d = ezr.xdist(tbl, target_row, row)
        distances.append((i, d))
    
    # Sort by distance (ascending)
    distances.sort(key=lambda x: x[1])
    
    # Return indices of the top k
    return [idx for idx, d in distances[:k]]

def remember(header, rows):
    """
    Returns the indices of the 5% of rows most similar to a representative 
    'ideal' employee (one with high tenure).
    """
    # Define an ideal employee: high tenure, low attrition
    # We use the top 5% of rows as defined by step01 logic
    tbl = ezr.Tbl([header] + rows)
    
    # Sort by ydist to find the 'best' (most stable) employees
    indexed_rows = list(enumerate(rows))
    indexed_rows.sort(key=lambda x: ezr.ydist(tbl, x[1]))
    
    # Pick the top 1 as our 'representative'
    representative = rows[indexed_rows[0][0]]
    
    # Find the 5% most similar to this representative
    limit = max(1, int(len(rows) * 0.05))
    similar_indices = find_similar(header, rows, representative, k=limit)
    
    return similar_indices

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    indices = remember(header, rows)
    
    print(f"Analysis of {len(rows)} records.")
    print(f"Identified {len(indices)} employees most similar to top-performing staff.")
    
    tenure_idx = header.index("YearsAtCompany+")
    print("\nSample of similar employees and their tenure:")
    for i in indices[:5]:
        print(f"Row {i}: {rows[i][tenure_idx]} years at company")
        
    exit(0)
