import csv
from step01 import remember as step01_remember

def find_similar(header, rows, target_row, k=5):
    """
    Finds the k most similar rows to the target_row using Euclidean distance
    on input columns.
    """
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    def dist(r1, r2):
        d = 0
        for i in input_indices:
            d += (r1[i] - r2[i])**2
        return d**0.5

    # Calculate distances to all rows
    distances = []
    for i, row in enumerate(rows):
        # Skip if row is the target itself
        if row == target_row:
            continue
        distances.append((dist(target_row, row), i))
    
    distances.sort()
    return [idx for _, idx in distances[:k]]

def remember(header, rows):
    """
    Returns the indices of the top 5% of rows based on goal performance.
    """
    return step01_remember(header, rows)

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', newline='') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(x) for x in row])
            
            # Use the first row as the "proposed setup"
            proposed = rows[0]
            
            # Find similar past setups
            similar_indices = find_similar(header, rows, proposed)
            
            print("Customer Inquiry: Show me past setups most like my proposal and how they turned out.")
            print(f"Proposed setup inputs: {proposed[:len(header)-3]}")
            print("\nMost similar past setups:")
            for idx in similar_indices:
                goals = {header[i]: rows[idx][i] for i in range(len(header)) 
                         if header[i].endswith(('-', '+'))}
                print(f"  Row {idx}: {goals}")
            
            # Identify best rows
            best_indices = remember(header, rows)
            print(f"\nNote: There are {len(best_indices)} top-performing setups in our database.")
            print(f"The best setup index is: {best_indices[0]}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
