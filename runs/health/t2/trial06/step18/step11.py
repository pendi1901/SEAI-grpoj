import csv
from step01 import remember as base_remember

def get_dist(row1, row2, input_indices):
    """Calculates distance between two rows based on input columns."""
    d = 0
    for i in input_indices:
        if isinstance(row1[i], str):
            d += 0 if row1[i] == row2[i] else 1
        else:
            # Normalize numeric distance by range if possible, 
            # but simple abs diff is sufficient for relative similarity
            d += abs(row1[i] - row2[i])
    return d

def remember(header, rows):
    """
    Finds the top 5% of rows using the base logic, 
    but for the customer's specific request, we identify 
    the most similar setups to the first row in the dataset.
    """
    # Identify input columns (those not ending in - or +)
    input_indices = [i for i, h in enumerate(header) 
                     if not (h.endswith('-') or h.endswith('+'))]
    
    # The customer asks for setups most like the one the team uses today (row 0)
    target_row = rows[0]
    
    # Calculate distances to all other rows
    distances = []
    for i in range(1, len(rows)):
        dist = get_dist(target_row, rows[i], input_indices)
        distances.append((dist, i))
    
    # Sort by distance (ascending) to find the most similar
    distances.sort(key=lambda x: x[0])
    
    # Return the indices of the top 5% most similar rows
    limit = max(1, len(rows) // 20)
    return [idx for dist, idx in distances[:limit]]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [val if header[i] == 'criterion' else float(val) 
                             for i, val in enumerate(row)]
            rows.append(processed_row)
            
    best_indices = remember(header, rows)
    
    print("The setups most similar to the team's current configuration are:")
    for idx in best_indices:
        # Calculate a simple score for display
        mre = rows[idx][0]
        acc = rows[idx][1]
        pred = rows[idx][2]
        score = (1 - mre) + acc + pred
        print(f" - Row {idx}: Score {score:.4f} (MRE: {mre:.4f}, ACC: {acc:.4f}, PRED40: {pred:.4f})")
