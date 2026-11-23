import csv

def spot(header, rows):
    """
    Identifies rows that are outliers in the input space.
    We calculate the mean and standard deviation for each input column,
    then flag rows that have values significantly far from the mean 
    (e.g., > 3 standard deviations).
    """
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    # Calculate means and std devs for inputs
    stats = []
    for i in input_indices:
        vals = [float(row[i]) for row in rows]
        mean = sum(vals) / len(vals)
        std = (sum((x - mean)**2 for x in vals) / len(vals))**0.5
        stats.append((i, mean, std))
    
    # Score rows based on how many standard deviations they are from the mean
    # across all input columns.
    scores = []
    for row_idx, row in enumerate(rows):
        total_z = 0
        for i, mean, std in stats:
            if std > 0:
                val = float(row[i])
                total_z += abs((val - mean) / std)
        scores.append((total_z, row_idx))
    
    # Sort by total_z descending (most suspicious first)
    scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return indices of rows that are extreme outliers (e.g., top 5%)
    limit = max(1, len(rows) // 20)
    return [item[1] for item in scores[:limit]]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
            
        suspicious_indices = spot(header, rows)
        
        print("Analysis complete. The following rows contain input values that appear to be outliers:")
        for idx in suspicious_indices[:5]:
            print(f"Row index {idx} is highly suspicious.")
            
        if len(suspicious_indices) > 5:
            print(f"... and {len(suspicious_indices) - 5} others.")
            
        exit(0)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
