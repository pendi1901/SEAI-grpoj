import csv

def spot(header, rows):
    """
    Identifies rows that are outliers in the input space.
    We calculate the distance of each row from the median of the dataset.
    Rows that are significantly distant from the median in the input space
    are considered 'unseen' or suspicious.
    """
    input_indices = [i for i, name in enumerate(header) if not (name.endswith(('-', '+')))]
    
    # Calculate the median for each input column to establish a 'typical' row
    medians = []
    for i in input_indices:
        vals = sorted([r[i] for r in rows if isinstance(r[i], (int, float))])
        if vals:
            medians.append(vals[len(vals) // 2])
        else:
            medians.append(0)
    
    # Calculate distance of each row from the median row
    # We use Euclidean distance on normalized inputs
    scores = []
    for row_idx, row in enumerate(rows):
        dist = 0
        for j, col_idx in enumerate(input_indices):
            val = row[col_idx]
            if isinstance(val, (int, float)):
                # Normalized distance from median
                dist += (val - medians[j]) ** 2
        scores.append((dist, row_idx))
    
    # Sort by distance descending (most suspicious/unseen first)
    scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return the top 5% of most suspicious rows
    limit = max(1, len(rows) // 20)
    return [item[1] for item in scores[:limit]]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        rows = []
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                processed_row = []
                for val in row:
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)
        
        suspicious = spot(header, rows)
        
        print("Analysis: Identifying setups that are unlike anything we have seen.")
        print(f"Identified {len(suspicious)} rows that deviate significantly from historical patterns.")
        print("The following row indices are the most suspicious (most 'unseen'):")
        print(suspicious[:10])
        print("These configurations are outliers in the input space and should be reviewed.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
