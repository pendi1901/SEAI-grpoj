import csv
import step01

def remember(header, rows):
    """
    Identifies the top 5% of rows based on goal performance.
    Uses the logic established in step01.
    """
    return step01.remember(header, rows)

def find_similar(header, rows, target_row, k=3):
    """
    Finds the k most similar rows to the target_row based on Euclidean distance
    of input columns.
    """
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    def dist(r1, r2):
        d = 0
        for i in input_indices:
            d += (r1[i] - r2[i])**2
        return d**0.5

    distances = []
    for i, row in enumerate(rows):
        distances.append((dist(row, target_row), i))
    
    distances.sort()
    return distances[:k]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rows.append([float(x) for x in row])

    # Pick a sample row to act as the "proposed" setup
    target_row = rows[0]
    
    # Find similar past setups
    similar = find_similar(header, rows[1:], target_row)
    
    print("Customer Inquiry: Here is the setup I am about to propose.")
    print("Analysis: Searching for past setups most similar to your proposal...")
    
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    
    for d, idx in similar:
        actual_idx = idx + 1
        row = rows[actual_idx]
        print(f"\nFound similar setup (Row {actual_idx}):")
        for g_idx in goal_indices:
            print(f"  {header[g_idx]}: {row[g_idx]:.4f}")
            
    print("\nThese past configurations are the closest matches in our database.")
