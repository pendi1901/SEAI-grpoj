import ezr
import random

def spot(header, rows):
    """
    Identify rows that contain input values 'far outside' what has been seen.
    We define 'suspicious' as rows containing values that are outliers 
    relative to the distribution of that column across the entire dataset.
    """
    # Create a table to handle column roles and normalization
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # For each column, calculate the range of seen values.
    # For numeric, we use the mean and standard deviation to find outliers.
    # For symbolic, we check if a value is rare (frequency < 1%).
    
    suspiciousness = []
    
    for i, row in enumerate(rows):
        score = 0
        for col in tbl.x:
            val = row[col.at]
            if val == "?":
                continue
            
            if isinstance(col, ezr.Num):
                # Z-score based outlier detection
                if col.sd > 0:
                    z = abs(val - col.mu) / col.sd
                    if z > 3:  # More than 3 standard deviations
                        score += z
            else:
                # Frequency based outlier detection
                total = col.n
                count = col.has.get(val, 0)
                if total > 0 and (count / total) < 0.01:
                    score += (1.0 - (count / total))
        
        if score > 0:
            suspiciousness.append((score, i))
    
    # Sort by score descending (higher score = more suspicious)
    suspiciousness.sort(key=lambda x: x[0], reverse=True)
    
    return [idx for _, idx in suspiciousness]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    try:
        data = list(ezr.csv(filename))
        header = data[0]
        rows = data[1:]
        
        # Get suspicious rows
        indices = spot(header, rows)
        
        print("Analysis: Identifying rows with settings far outside historical norms.")
        if not indices:
            print("No suspicious rows found.")
        else:
            print(f"Found {len(indices)} potentially anomalous rows.")
            print("Top 5 most suspicious indices:")
            for i in range(min(5, len(indices))):
                idx = indices[i]
                print(f"Row {idx}: {rows[idx]}")
            
        print("\nThese rows contain input values that are statistical outliers.")
        exit(0)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
