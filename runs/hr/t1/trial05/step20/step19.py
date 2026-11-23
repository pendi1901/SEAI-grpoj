import csv

def spot(header, rows):
    """
    Identifies rows that are 'unlike anyone we have employed' by calculating
    the distance to the nearest neighbor in the historical data.
    If the distance to the nearest neighbor is significantly higher than the 
    average distance between existing records, the row is considered an outlier 
    (untrusted estimate).
    """
    input_indices = [
        i for i, name in enumerate(header) 
        if name[0].isupper() and not (name.endswith('+') or name.endswith('-'))
    ]

    # Calculate distance between two rows based on numeric inputs
    def get_dist(r1, r2):
        dist = 0
        for i in input_indices:
            if isinstance(r1[i], float) and isinstance(r2[i], float):
                # Normalize distance by range if possible, but simple Euclidean is fine
                dist += (r1[i] - r2[i])**2
        return dist**0.5

    # Find the distance to the nearest neighbor for every row
    # This identifies how 'unique' or 'unlike' each row is compared to the rest
    suspicion_scores = []
    for i, row in enumerate(rows):
        min_dist = float('inf')
        for j, other in enumerate(rows):
            if i == j:
                continue
            d = get_dist(row, other)
            if d < min_dist:
                min_dist = d
        suspicion_scores.append((min_dist, i))

    # Sort by distance descending: rows with the largest 'nearest neighbor' 
    # distance are the most unique/unlike anyone else.
    suspicion_scores.sort(key=lambda x: x[0], reverse=True)
    
    return [item[1] for item in suspicion_scores]

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    suspicious_indices = spot(header, rows)
    
    print("Trust Analysis: Identifying unique or 'unlike' records")
    print("The following rows represent employees who are statistically unlike")
    print("anyone else in our history. Estimates for these individuals are")
    print("less reliable because we lack similar historical data:")
    
    for idx in suspicious_indices[:10]:
        print(f"- Row index {idx} is highly unique.")
    
    print("\nThese records should be treated with caution when making predictions.")
