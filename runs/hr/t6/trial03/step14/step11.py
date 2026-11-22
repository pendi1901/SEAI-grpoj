import ezr
import random

def find_similar(header, rows, target_row, k=5):
    """
    Finds the k most similar rows to target_row based on input columns (x).
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate xdist between target_row and all other rows
    distances = []
    for i, row in enumerate(rows):
        # Skip comparing the row to itself if it exists in the dataset
        if row == target_row:
            continue
        d = ezr.xdist(tbl, target_row, row)
        distances.append((d, i))
    
    # Sort by distance ascending (most similar first)
    distances.sort(key=lambda x: x[0])
    
    return [idx for d, idx in distances[:k]]

def remember(header, rows):
    """
    Returns the indices of the 5% of rows most similar to the first row 
    in the dataset, as a proxy for 'people most like them'.
    """
    # Per requirements: return at most 5% of rows (800 * 0.05 = 40)
    limit = max(1, int(len(rows) * 0.05))
    
    # Use the first row as the target 'employee'
    target = rows[0]
    
    # Get indices of similar rows
    similar_indices = find_similar(header, rows, target, k=limit)
    
    return similar_indices

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Get similar records
    indices = remember(header, rows)
    
    # Identify tenure columns (ending in +)
    tenure_cols = [i for i, name in enumerate(header) if name.endswith("+")]
    
    print("Similarity Analysis: Employees most like the target record.")
    print(f"Found {len(indices)} similar records.")
    print("-" * 60)
    
    for idx in indices:
        row = rows[idx]
        tenure_info = ", ".join([f"{header[c]}: {row[c]}" for c in tenure_cols])
        print(f"Record {idx}: {tenure_info}")
        
    print("-" * 60)
    print("These records were identified by calculating the Euclidean distance")
    print("across all input attributes (x-columns).")
    
    exit(0)
