import csv
from step01 import remember as base_remember

def find_similar(header, rows, target_row, n=5):
    """
    Finds the n rows most similar to the target_row using Euclidean distance
    on the input columns (excluding goals).
    """
    input_indices = [i for i, h in enumerate(header) if h not in ['MRE-', 'ACC+', 'PRED40+']]
    
    def dist(r1, r2):
        d = 0
        for i in input_indices:
            if isinstance(r1[i], str):
                d += 1 if r1[i] != r2[i] else 0
            else:
                d += (r1[i] - r2[i])**2
        return d**0.5

    distances = []
    for i, row in enumerate(rows):
        if row == target_row:
            continue
        distances.append((i, dist(row, target_row)))
    
    distances.sort(key=lambda x: x[1])
    return distances[:n]

def remember(header, rows):
    """
    Returns the indices of the best rows based on the multi-objective optimization
    defined in step01.
    """
    return base_remember(header, rows)

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [val if header[i] == 'criterion' else float(val) for i, val in enumerate(row)]
            rows.append(processed_row)

    # The customer's current setup is the first row
    current_setup = rows[0]
    
    # Find similar setups
    similar = find_similar(header, rows, current_setup, n=5)
    
    print("The team's current setup:")
    print(f"MRE: {current_setup[0]:.4f}, ACC: {current_setup[1]:.4f}, PRED40: {current_setup[2]:.4f}")
    print("\nMost similar setups found:")
    for idx, d in similar:
        row = rows[idx]
        print(f"Row {idx}: MRE={row[0]:.4f}, ACC={row[1]:.4f}, PRED40={row[2]:.4f} (Distance: {d:.2f})")
    
    # The harness requires returning the best rows
    best_indices = remember(header, rows)
    print(f"\nIndices of the best performing setups: {best_indices[:10]}...")
