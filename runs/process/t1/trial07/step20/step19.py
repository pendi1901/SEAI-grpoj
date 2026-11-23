import csv

def spot(header, rows):
    """
    Identifies rows that are outliers in the input space.
    We calculate the centroid of the input columns and return the indices 
    of rows sorted by their Euclidean distance from that centroid.
    """
    # Identify input columns (those not ending in - or +)
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    num_rows = len(rows)
    if num_rows == 0:
        return []
    
    # Calculate the centroid of the input space
    centroid = []
    for i in input_indices:
        col_vals = [row[i] for row in rows if isinstance(row[i], (int, float))]
        if col_vals:
            centroid.append(sum(col_vals) / len(col_vals))
        else:
            centroid.append(0.0)
    
    # Calculate distance of each row from the centroid
    # Rows with high distance are considered "unseen" or outliers
    distances = []
    for idx, row in enumerate(rows):
        dist_sq = 0.0
        count = 0
        for i, col_idx in enumerate(input_indices):
            if isinstance(row[col_idx], (int, float)):
                dist_sq += (row[col_idx] - centroid[i]) ** 2
                count += 1
        
        # Normalize distance by number of valid inputs
        if count > 0:
            distances.append(((dist_sq / count)**0.5, idx))
        else:
            distances.append((0.0, idx))
    
    # Sort by distance descending (most suspicious/unseen first)
    distances.sort(key=lambda x: x[0], reverse=True)
    
    return [item[1] for item in distances]

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed_row = []
                for val in row:
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)
        
        suspicious_indices = spot(header, rows)
        
        print("Customer Inquiry: Identifying Unseen/Anomalous Setups")
        print("-" * 60)
        print("The following row indices represent configurations that are")
        print("most unlike the historical data we have seen so far:")
        print(suspicious_indices[:10])
        print("\nThese setups deviate significantly from the average input")
        print("patterns, suggesting they are novel or potentially erroneous.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
