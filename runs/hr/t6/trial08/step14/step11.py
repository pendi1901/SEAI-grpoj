import ezr
import step01

def find_similar(header, rows, target_row, k=5):
    """
    Finds the k rows most similar to target_row based on input columns (x).
    """
    tbl = ezr.Tbl([header] + rows)
    # Calculate distance from target_row to all other rows
    scored = []
    for i, row in enumerate(rows):
        # Skip comparing to self
        if row == target_row:
            continue
        d = ezr.xdist(tbl, target_row, row)
        scored.append((d, i))
    
    # Sort by distance ascending (most similar first)
    scored.sort(key=lambda x: x[0])
    return scored[:k]

def remember(header, rows):
    """
    Returns the indices of the 5% of rows most similar to the first row,
    as a proxy for 'people most like them'.
    """
    target = rows[0]
    limit = max(1, int(len(rows) * 0.05))
    
    tbl = ezr.Tbl([header] + rows)
    scored = []
    for i, row in enumerate(rows):
        d = ezr.xdist(tbl, target, row)
        scored.append((d, i))
    
    scored.sort(key=lambda x: x[0])
    return [idx for d, idx in scored[:limit]]

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    target_idx = 0
    target_row = rows[target_idx]
    
    # Find similar rows
    similar_indices = remember(header, rows)
    
    # Identify tenure columns (ending in +)
    tenure_cols = [i for i, name in enumerate(header) if name.endswith('+')]
    
    print(f"Analysis: Employees most similar to row {target_idx}")
    print("-" * 60)
    print(f"{'Index':<10} | {'Tenure (YearsAtCompany)':<25}")
    print("-" * 60)
    
    for idx in similar_indices:
        row = rows[idx]
        # YearsAtCompany is index 31
        tenure = row[31]
        print(f"{idx:<10} | {tenure:<25}")
        
    print("-" * 60)
    print("These employees were identified based on input column similarity.")
