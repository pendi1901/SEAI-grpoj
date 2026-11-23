import csv
import step01
import step02

def remember(header, rows):
    """
    Identifies the top 5% of rows based on multi-objective optimization.
    Uses the logic from step01 to rank rows and return the indices of the best ones.
    """
    return step01.remember(header, rows)

def find_similar(header, rows, target_row, n=5):
    """
    Finds the 'n' most similar rows to the target_row based on input columns.
    Uses the distance metric from step02.
    """
    input_indices = [i for i, h in enumerate(header) if h not in ['MRE-', 'ACC+', 'PRED40+']]
    
    # Calculate ranges for normalization
    mins = []
    maxs = []
    for i in input_indices:
        vals = [r[i] for r in rows if isinstance(r[i], (int, float))]
        mins.append(min(vals) if vals else 0)
        maxs.append(max(vals) if vals else 1)

    def distance(r1, r2):
        d = 0
        for j, idx in enumerate(input_indices):
            v1, v2 = r1[idx], r2[idx]
            if isinstance(v1, str):
                d += 1 if v1 != v2 else 0
            else:
                d += ((v1 - v2) / (maxs[j] - mins[j] + 1e-9))**2
        return d**0.5

    # Calculate distances to all rows
    dists = []
    for i, row in enumerate(rows):
        dists.append((i, distance(target_row, row)))
    
    # Return indices of the n closest rows
    return sorted(dists, key=lambda x: x[1])[1:n+1]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [val if header[i] == 'criterion' else float(val) for i, val in enumerate(row)]
            rows.append(processed_row)

    # Assume the team's current setup is the last row in the dataset
    current_setup = rows[-1]
    
    # Find similar setups
    similar = find_similar(header, rows, current_setup)
    
    print("The team's current setup (last row) compared to similar configurations:")
    print(f"Current Setup: MRE={current_setup[0]:.4f}, ACC={current_setup[1]:.4f}, PRED40={current_setup[2]:.4f}")
    print("-" * 50)
    for idx, dist in similar:
        row = rows[idx]
        print(f"Row {idx} (Dist: {dist:.4f}): MRE={row[0]:.4f}, ACC={row[1]:.4f}, PRED40={row[2]:.4f}")
